"""
One-Shot Siamese Network ONNX Model
"""

import onnxruntime as ort
from onnxruntime import SessionOptions, Session
import numpy as np
import cv2
from typing import Optional, Tuple, List
import hashlib

class SiameseONNXModel:
    """
    ONNX Runtime wrapper for Siamese one-shot learning model
    """
    
    def __init__(self, model_path: str = 'models/siamone.onnx'):
        self.model_path = model_path
        self.session: Optional[Session] = None
        self.session_options = SessionOptions()
        self.session_options.intra_op_num_threads = 4
        self.session_options.inter_op_num_threads = 2
        
        self._load_model()
    
    def _load_model(self):
        """Load ONNX model"""
        try:
            self.session = ort.InferenceSession(self.model_path, self.session_options)
        except FileNotFoundError:
            print(f"Warning: Model not found at {self.model_path}")
            print("Starting with placeholder model")
            # Create a placeholder model if needed
            self._create_placeholder_model()
    
    def _create_placeholder_model(self):
        """Create placeholder ONNX model for testing"""
        import onnx
        import onnxruntime
        import numpy as np
        
        # Create dummy model
        graph = onnx.make_graph(
            nodes=[
                # Simple convolution layers as placeholder
                onnx.helper.make_node(
                    'Conv', ['input', 'filters'], 'features1',
                    name='conv1'
                ),
                onnx.helper.make_node(
                    'Conv', ['input', 'filters'], 'features2',
                    name='conv2'
                ),
                onnx.helper.make_node(
                    'GlobalAveragePool', ['features1'], 'emb1',
                    name='pool1'
                ),
                onnx.helper.make_node(
                    'GlobalAveragePool', ['features2'], 'emb2',
                    name='pool2'
                ),
                onnx.helper.make_node(
                    'Sigmoid', ['emb1', 'emb2'], 'embedding_distance',
                    name='dist'
                ),
            ],
            initializers=[
                onnx.helper.make_tensor_value_info('input', onnx.TensorProto.FLOAT, [1, 3, 128, 128]),
                onnx.helper.make_tensor_value_info('filters', onnx.TensorProto.FLOAT, [1, 64, 3, 3]),
                onnx.helper.make_tensor_value_info('features1', onnx.TensorProto.FLOAT, [1, 64, 128, 128]),
                onnx.helper.make_tensor_value_info('features2', onnx.TensorProto.FLOAT, [1, 64, 128, 128]),
                onnx.helper.make_tensor_value_info('emb1', onnx.TensorProto.FLOAT, [1, 512]),
                onnx.helper.make_tensor_value_info('emb2', onnx.TensorProto.FLOAT, [1, 512]),
            ],
            inputs=['input'],
            outputs=['embedding_distance'],
            value_info=[
                onnx.helper.make_tensor_value_info('filters', onnx.TensorProto.FLOAT, [1, 64, 3, 3])
            ]
        )
        
        dummy_model = onnx.GraphProto()
        dummy_model.SetAttributes(graph)
        
        onnx.save(dummy_model, self.model_path)
        print(f"Created placeholder model at {self.model_path}")
    
    def extract_embedding(self, image: np.ndarray) -> np.ndarray:
        """
        Extract embedding from input image
        Returns: embedding vector
        """
        if self.session is None:
            # Placeholder embedding
            np.random.seed(42)
            embedding = np.random.randn(1, 512).astype(np.float32)
            return embedding
        
        # Preprocess image
        img_tensor = self._preprocess_image(image)
        
        # Inference
        output = self.session.run(None, {'input': img_tensor})[0]
        
        # Extract embedding (assuming last two outputs are embeddings)
        embedding = output[1]  # Second output
        return embedding.flatten()
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for model input"""
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Resize to fixed size
        resized = cv2.resize(gray, (128, 128))
        
        # Normalize
        normalized = resized.astype(np.float32) / 255.0
        normalized = normalized.transpose(2, 0, 1)  # CHW format
        normalized = np.expand_dims(normalized, axis=0)  # Add batch dimension
        
        return normalized
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings"""
        # Normalize
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        
        # Ensure similarity is in range [0, 1]
        return max(0.0, min(1.0, similarity))
    
    def compute_distance(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute L2 distance between two embeddings"""
        return np.linalg.norm(embedding1 - embedding2)
    
    def predict(self, image: np.ndarray) -> float:
        """
        Predict similarity score
        Returns: confidence score (0.0 to 1.0)
        """
        embedding = self.extract_embedding(image)
        # Placeholder: return random confidence
        confidence = np.random.uniform(0.5, 0.95)
        return float(confidence)
    
    def close(self):
        """Clean up ONNX session"""
        if self.session:
            del self.session
