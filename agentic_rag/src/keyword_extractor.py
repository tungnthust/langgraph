"""
Keyword extraction module using Vietnamese NER models.
Supports configurable NER models from HuggingFace.
"""
from typing import List, Set
import re


class KeywordExtractor:
    """Extract keywords from Vietnamese text using NER models"""
    
    def __init__(self, model_name: str = "NlpHUST/ner-vietnamese-electra-base", 
                 device: str = "cuda", enabled: bool = True):
        self.enabled = enabled
        self.model = None
        self.tokenizer = None
        
        if self.enabled:
            try:
                from transformers import AutoTokenizer, AutoModelForTokenClassification
                import torch
                
                print(f"Loading NER model: {model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForTokenClassification.from_pretrained(model_name)
                
                # Move to device
                self.device = device if torch.cuda.is_available() and device == "cuda" else "cpu"
                self.model.to(self.device)
                self.model.eval()
                
                print(f"NER model loaded on {self.device}")
            except Exception as e:
                print(f"Warning: Failed to load NER model: {e}")
                print("Falling back to simple keyword extraction")
                self.enabled = False
    
    def extract_keywords(self, text: str, max_keywords: int = 20) -> List[str]:
        """
        Extract keywords from text using NER model or fallback methods.
        
        Args:
            text: Input text to extract keywords from
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of extracted keywords
        """
        if not text or not text.strip():
            return []
        
        if self.enabled and self.model is not None:
            return self._extract_with_ner(text, max_keywords)
        else:
            return self._extract_simple(text, max_keywords)
    
    def _extract_with_ner(self, text: str, max_keywords: int) -> List[str]:
        """Extract keywords using NER model"""
        try:
            import torch
            
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.argmax(outputs.logits, dim=-1)
            
            # Decode tokens and extract entities
            tokens = self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
            predictions = predictions[0].cpu().numpy()
            
            # Extract named entities
            keywords = set()
            current_entity = []
            
            for token, pred in zip(tokens, predictions):
                # Skip special tokens
                if token in ['[CLS]', '[SEP]', '[PAD]']:
                    continue
                
                # Check if this is an entity (non-O tag)
                if pred != 0:  # Assuming 0 is 'O' (outside entity)
                    # Clean token
                    token_clean = token.replace('##', '')
                    current_entity.append(token_clean)
                else:
                    # End of entity
                    if current_entity:
                        entity = ''.join(current_entity)
                        if len(entity) > 1:  # Filter out single characters
                            keywords.add(entity)
                        current_entity = []
            
            # Add last entity if exists
            if current_entity:
                entity = ''.join(current_entity)
                if len(entity) > 1:
                    keywords.add(entity)
            
            # Also add important words as fallback
            keywords.update(self._extract_important_words(text, max_keywords // 2))
            
            return list(keywords)[:max_keywords]
            
        except Exception as e:
            print(f"Warning: NER extraction failed: {e}")
            return self._extract_simple(text, max_keywords)
    
    def _extract_simple(self, text: str, max_keywords: int) -> List[str]:
        """
        Simple keyword extraction as fallback.
        Extracts capitalized words, numbers, and important Vietnamese terms.
        """
        keywords = set()
        
        # Extract capitalized words (potential proper nouns)
        capitalized = re.findall(r'\b[A-ZÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ][a-zàáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+', text)
        keywords.update(capitalized)
        
        # Extract important words
        keywords.update(self._extract_important_words(text, max_keywords))
        
        return list(keywords)[:max_keywords]
    
    def _extract_important_words(self, text: str, max_words: int) -> Set[str]:
        """
        Extract important words based on frequency and characteristics.
        Captures Vietnamese technical terms and important keywords.
        """
        # Vietnamese stop words (common words to filter out)
        stop_words = {
            'là', 'và', 'của', 'có', 'được', 'trong', 'cho', 'để', 'với', 'không',
            'này', 'các', 'một', 'đã', 'như', 'từ', 'hoặc', 'khi', 'về', 'theo',
            'sẽ', 'thì', 'hay', 'bởi', 'cũng', 'đến', 'những', 'nhiều', 'nếu', 'vì'
        }
        
        # Split into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter and count
        word_freq = {}
        for word in words:
            if len(word) > 2 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top words by frequency
        important = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Also include single occurrence but long words (technical terms)
        for word in words:
            if len(word) >= 6 and word not in stop_words:
                if word not in [w[0] for w in important]:
                    important.append((word, 1))
        
        return set([word for word, _ in important[:max_words]])
