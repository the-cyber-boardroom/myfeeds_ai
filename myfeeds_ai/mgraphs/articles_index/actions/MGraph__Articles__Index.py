
class MGraph__Articles__Index():
    """Provider for managing article indexes"""

    def __init__(self):
        super().__init__()
        self.graph.model.data.schema_types = Schema__Article__Index__Types()

    def add_article(self, article_data: Dict[str, Any], article_path: str) -> Optional[Obj_Id]:
        """Add or update article in the index"""
        with self.edit() as edit:
            # Create article index node
            article_node = edit.new_node(
                node_data = Schema__Article__Index__Node__Data(
                    article_id     = article_data['article_id'],
                    article_obj_id = article_data['article_obj_id'],
                    title         = article_data['title'],
                    path          = article_path,
                    timestamp_utc = article_data['when']['timestamp_utc']
                )
            )
            return article_node.node_id if article_node else None

    def has_article(self, article_obj_id: str) -> Optional[str]:
        """Check if article exists and return its path if found"""
        with self.data() as data:
            # Use the index to find nodes with matching article_obj_id
            for node in data.nodes():
                if node.node_data.article_obj_id == article_obj_id:
                    return node.node_data.path
        return None

    def get_articles_in_timeframe(self, start_timestamp: int, end_timestamp: int) -> list[str]:
        """Get paths of articles within a specific timeframe"""
        article_paths = []
        with self.data() as data:
            for node in data.nodes():
                timestamp = node.node_data.timestamp_utc
                if start_timestamp <= timestamp <= end_timestamp:
                    article_paths.append(node.node_data.path)
        return article_paths