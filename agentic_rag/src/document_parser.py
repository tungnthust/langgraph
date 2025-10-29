"""
Intelligent document parser for Vietnamese technical documents.
Handles markdown with complex HTML tables and metadata extraction.
"""
import re
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    """Represents a chunk of document with metadata"""
    content: str  # Original content with HTML
    content_for_embedding: str  # Content with HTML tags removed for embedding
    metadata: Dict[str, any]
    chunk_id: str
    chunk_type: str  # 'text' or 'table'


class DocumentParser:
    """Parse markdown documents with intelligent chunking and metadata extraction"""
    
    def __init__(self, text_chunk_size: int = 512, text_chunk_overlap: int = 64,
                 table_max_rows: int = 20, table_min_rows_for_split: int = 25):
        self.text_chunk_size = text_chunk_size
        self.text_chunk_overlap = text_chunk_overlap
        self.table_max_rows = table_max_rows
        self.table_min_rows_for_split = table_min_rows_for_split
    
    def parse_document(self, file_path: Path) -> List[DocumentChunk]:
        """Parse a markdown document into intelligent chunks"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract filename and title from the first lines
        filename, title = self._extract_metadata(content)
        
        # Split document into sections and elements
        chunks = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip metadata lines
            if i < 5 and (line.startswith('*Filename*:') or line.startswith('*TITLE*:')):
                i += 1
                continue
            
            # Check if this is a table
            if '<table>' in line or (i < len(lines) - 1 and '<table>' in lines[i + 1]):
                # Find table end
                table_lines, table_end_idx = self._extract_table(lines, i)
                table_html = '\n'.join(table_lines)
                
                # Find table title (usually before the table)
                table_title = self._find_table_title(lines, i)
                
                # Get current heading context
                current_heading = self._get_current_heading(lines, i)
                
                # Parse and chunk table
                table_chunks = self._chunk_table(
                    table_html, filename, title, table_title, current_heading
                )
                chunks.extend(table_chunks)
                
                i = table_end_idx + 1
            else:
                # Process text content
                text_section, section_end_idx = self._extract_text_section(lines, i)
                if text_section.strip():
                    current_heading = self._get_current_heading(lines, i)
                    text_chunks = self._chunk_text(
                        text_section, filename, title, current_heading
                    )
                    chunks.extend(text_chunks)
                i = section_end_idx + 1
        
        # Add chunk position metadata
        for idx, chunk in enumerate(chunks):
            chunk.metadata['chunk_position'] = idx
            chunk.metadata['total_chunks'] = len(chunks)
        
        return chunks
    
    def _extract_metadata(self, content: str) -> Tuple[str, str]:
        """Extract filename and title from document"""
        lines = content.split('\n')
        filename = ""
        title = ""
        
        for line in lines[:10]:
            if line.startswith('*Filename*:'):
                filename = line.split(':', 1)[1].strip()
            elif line.startswith('*TITLE*:'):
                title = line.split(':', 1)[1].strip()
        
        return filename, title
    
    def _extract_table(self, lines: List[str], start_idx: int) -> Tuple[List[str], int]:
        """Extract table HTML from lines"""
        table_lines = []
        i = start_idx
        in_table = False
        
        while i < len(lines):
            line = lines[i]
            if '<table>' in line:
                in_table = True
            
            if in_table:
                table_lines.append(line)
            
            if '</table>' in line:
                break
            
            i += 1
        
        return table_lines, i
    
    def _find_table_title(self, lines: List[str], table_start_idx: int) -> Optional[str]:
        """Find table title by looking at lines before the table"""
        # Look up to 5 lines before the table
        for i in range(max(0, table_start_idx - 5), table_start_idx):
            line = lines[i].strip()
            # Table titles often contain "Bảng" or "Table"
            if line and ('Bảng' in line or 'Table' in line or 'BẢNG' in line):
                # Clean and return
                return line
        return None
    
    def _get_current_heading(self, lines: List[str], current_idx: int) -> Optional[str]:
        """Get the current section heading by looking backwards"""
        headings = []
        for i in range(current_idx - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith('#'):
                # Extract heading level and text
                level = len(line) - len(line.lstrip('#'))
                heading_text = line.lstrip('#').strip()
                headings.insert(0, (level, heading_text))
                # If we found a top-level heading, stop
                if level == 1:
                    break
        
        if headings:
            # Join headings hierarchically
            return ' > '.join([h[1] for h in headings])
        return None
    
    def _extract_text_section(self, lines: List[str], start_idx: int) -> Tuple[str, int]:
        """Extract a text section until we hit a table or significant break"""
        text_lines = []
        i = start_idx
        
        while i < len(lines):
            line = lines[i]
            
            # Stop if we hit a table
            if '<table>' in line:
                break
            
            text_lines.append(line)
            i += 1
            
            # Stop at next major section (but include current line)
            if i < len(lines) and lines[i].strip().startswith('# '):
                break
        
        return '\n'.join(text_lines), i - 1
    
    def _chunk_text(self, text: str, filename: str, title: str, 
                    heading: Optional[str]) -> List[DocumentChunk]:
        """Chunk text content intelligently"""
        chunks = []
        
        # Remove excessive newlines but preserve paragraph structure
        text = re.sub(r'\n{3,}', '\n\n', text.strip())
        
        if not text:
            return chunks
        
        # Split by paragraphs
        paragraphs = text.split('\n\n')
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_length = len(para)
            
            # If adding this paragraph exceeds chunk size
            if current_length + para_length > self.text_chunk_size and current_chunk:
                # Create chunk
                chunk_content = '\n\n'.join(current_chunk)
                chunks.append(self._create_text_chunk(
                    chunk_content, filename, title, heading, len(chunks)
                ))
                
                # Start new chunk with overlap
                overlap_text = current_chunk[-1] if current_chunk else ""
                current_chunk = [overlap_text, para] if overlap_text else [para]
                current_length = len(overlap_text) + para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        # Add remaining chunk
        if current_chunk:
            chunk_content = '\n\n'.join(current_chunk)
            chunks.append(self._create_text_chunk(
                chunk_content, filename, title, heading, len(chunks)
            ))
        
        return chunks
    
    def _create_text_chunk(self, content: str, filename: str, title: str,
                          heading: Optional[str], chunk_idx: int) -> DocumentChunk:
        """Create a text chunk with metadata"""
        # Content for embedding: same as original for text
        content_for_embedding = content
        
        chunk_id = f"{filename}_text_{chunk_idx}"
        
        metadata = {
            'filename': filename,
            'document_title': title,
            'section_heading': heading or "N/A",
            'chunk_type': 'text',
            'chunk_index_in_type': chunk_idx,
        }
        
        return DocumentChunk(
            content=content,
            content_for_embedding=content_for_embedding,
            metadata=metadata,
            chunk_id=chunk_id,
            chunk_type='text'
        )
    
    def _chunk_table(self, table_html: str, filename: str, title: str,
                     table_title: Optional[str], heading: Optional[str]) -> List[DocumentChunk]:
        """
        Intelligently chunk tables while preserving structure.
        - Maintains headers in each chunk
        - Avoids splitting after rows with colspan (parent sections)
        - Tracks chunk relationships for multi-part tables
        """
        soup = BeautifulSoup(table_html, 'html.parser')
        table = soup.find('table')
        
        if not table:
            return []
        
        # Extract headers (thead or first rows)
        headers = self._extract_table_headers(table)
        rows = table.find_all('tr')
        
        # Separate header rows from data rows
        header_rows = []
        data_rows = []
        
        # Find where headers end
        thead = table.find('thead')
        if thead:
            header_rows = thead.find_all('tr')
            tbody = table.find('tbody')
            if tbody:
                data_rows = tbody.find_all('tr')
            else:
                data_rows = [r for r in rows if r not in header_rows]
        else:
            # Heuristic: first few rows might be headers
            # Look for rows with <th> elements
            for row in rows:
                if row.find('th'):
                    header_rows.append(row)
                else:
                    data_rows.append(row)
            
            # If no <th> found, treat first row as header
            if not header_rows and rows:
                header_rows = [rows[0]]
                data_rows = rows[1:]
        
        total_data_rows = len(data_rows)
        
        # If table is small enough, return as single chunk
        if total_data_rows <= self.table_max_rows:
            return [self._create_table_chunk(
                table_html, filename, title, table_title, heading, 0, 1, False
            )]
        
        # Need to split table
        chunks = []
        chunk_idx = 0
        i = 0
        
        while i < total_data_rows:
            # Determine chunk size
            end_idx = min(i + self.table_max_rows, total_data_rows)
            
            # Avoid splitting right after a row with colspan
            # (it might be a section header)
            if end_idx < total_data_rows:
                # Look back a few rows to find a safe split point
                for check_idx in range(end_idx - 1, max(i, end_idx - 5), -1):
                    if not self._row_has_colspan(data_rows[check_idx]):
                        end_idx = check_idx + 1
                        break
            
            # Create chunk with headers + data rows
            chunk_rows = header_rows + data_rows[i:end_idx]
            chunk_html = self._reconstruct_table_html(table, chunk_rows)
            
            is_multi_part = total_data_rows > self.table_max_rows
            
            chunk = self._create_table_chunk(
                chunk_html, filename, title, table_title, heading,
                chunk_idx, None, is_multi_part
            )
            chunks.append(chunk)
            
            chunk_idx += 1
            i = end_idx
        
        # Update total parts in metadata
        total_parts = len(chunks)
        for chunk in chunks:
            chunk.metadata['table_total_parts'] = total_parts
        
        return chunks
    
    def _extract_table_headers(self, table) -> List[str]:
        """Extract table headers as text"""
        headers = []
        thead = table.find('thead')
        if thead:
            for th in thead.find_all('th'):
                headers.append(th.get_text(strip=True))
        else:
            # Try first row
            first_row = table.find('tr')
            if first_row:
                for cell in first_row.find_all(['th', 'td']):
                    headers.append(cell.get_text(strip=True))
        return headers
    
    def _row_has_colspan(self, row) -> bool:
        """Check if a row has cells with colspan (likely a section header)"""
        for cell in row.find_all(['td', 'th']):
            if cell.get('colspan'):
                return True
        return False
    
    def _reconstruct_table_html(self, original_table, rows: List) -> str:
        """Reconstruct table HTML with given rows"""
        # Create a new table with the same attributes
        soup = BeautifulSoup("<table></table>", 'html.parser')
        new_table = soup.find('table')
        
        # Copy attributes from original
        for attr, value in original_table.attrs.items():
            new_table[attr] = value
        
        # Add colgroup if exists in original
        colgroup = original_table.find('colgroup')
        if colgroup:
            new_table.append(colgroup)
        
        # Add rows
        for row in rows:
            new_table.append(row)
        
        return str(new_table)
    
    def _create_table_chunk(self, table_html: str, filename: str, title: str,
                           table_title: Optional[str], heading: Optional[str],
                           part_idx: int, total_parts: Optional[int],
                           is_multi_part: bool) -> DocumentChunk:
        """Create a table chunk with metadata"""
        # For embedding: remove HTML tags but keep structure
        soup = BeautifulSoup(table_html, 'html.parser')
        
        # Extract text from table for embedding
        content_for_embedding = []
        for row in soup.find_all('tr'):
            row_text = ' | '.join([cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])])
            if row_text:
                content_for_embedding.append(row_text)
        
        content_for_embedding = '\n'.join(content_for_embedding)
        
        # Add table title to embedding content if available
        if table_title:
            content_for_embedding = f"{table_title}\n\n{content_for_embedding}"
        
        chunk_id = f"{filename}_table_{part_idx}"
        
        metadata = {
            'filename': filename,
            'document_title': title,
            'section_heading': heading or "N/A",
            'table_title': table_title or "N/A",
            'chunk_type': 'table',
            'is_multi_part_table': is_multi_part,
            'table_part_index': part_idx,
            'table_total_parts': total_parts,
        }
        
        return DocumentChunk(
            content=table_html,  # Original HTML
            content_for_embedding=content_for_embedding,  # Clean text
            metadata=metadata,
            chunk_id=chunk_id,
            chunk_type='table'
        )
