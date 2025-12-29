import logging
from typing import Optional
from isanlp_rst.parser import Parser as RSTParser
from schemas import RSTNode

logger = logging.getLogger(__name__)

class DiscourseParser:
    def __init__(self):
        logger.info("Initializing RST Parser (gumrrg)...")
        # Initialize with English model 'gumrrg'
        # cuda_device=-1 for CPU. Change to 0 if GPU is available.
        self.parser = RSTParser(hf_model_name='tchewik/isanlp_rst_v3', 
                                hf_model_version='gumrrg', 
                                cuda_device=-1)
        logger.info("RST Parser initialized.")

    def parse(self, text: str) -> Optional[RSTNode]:
        if not text.strip():
            return None
            
        try:
            # The parser returns a dictionary with 'rst' key containing a list of trees
            res = self.parser(text)
            
            if not res.get('rst'):
                return None
                
            # We take the first tree (assuming document-level parsing)
            root = res['rst'][0]
            return self._convert_node(root)
        except Exception as e:
            logger.error(f"Error during parsing: {e}")
            raise e

    def _convert_node(self, node, node_id: int = 0) -> RSTNode:
        """
        Recursively convert isanlp node to RSTNode schema.
        """
        # isanlp nodes have 'left' and 'right' for binary trees
        children = []
        if hasattr(node, 'left') and node.left:
            children.append(self._convert_node(node.left, node_id * 2 + 1))
        if hasattr(node, 'right') and node.right:
            children.append(self._convert_node(node.right, node_id * 2 + 2))
            
        # Extract text if it's a leaf node (EDU)
        text = None
        if hasattr(node, 'text') and node.text:
            text = node.text
        elif not children:
            # Sometimes text might be stored differently or it's an EDU object
            # For now, we assume .text attribute exists on leaves
            pass

        return RSTNode(
            id=node_id,
            relation=getattr(node, 'relation', 'span'),
            nuclearity=getattr(node, 'nuclearity', 'flat'),
            text=text,
            start=getattr(node, 'start', None),
            end=getattr(node, 'end', None),
            children=children
        )
