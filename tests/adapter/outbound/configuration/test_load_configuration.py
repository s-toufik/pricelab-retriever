from unittest.mock import patch, MagicMock
from pricelab_retriever.adapter.outbound.configuration.load_configuration import LoadConfiguration
from pricelab_retriever.domain.model.app.app_configuration import AppConfiguration

FAKE_CONFIG = {
    "app_configuration": {
        "run": "async",
        "primary_database_type": "in_memory",
        "secondary_database_type": "in_disk",
        "data_providers": {},
        "data_use_cases": {}
    }
}


class TestLoadConfiguration:

    def _reset_loader(self, loader: LoadConfiguration):
        loader._cached_config = None

    def _mock_handler(self, mock_handler):
        mock_instance = MagicMock()
        mock_instance.read.return_value = FAKE_CONFIG
        mock_handler.return_value = mock_instance
        return mock_instance

    @patch("pricelab_retriever.adapter.outbound.configuration.load_configuration.Handler")
    def test_load_cache(self, mock_handler):
        mock_instance = self._mock_handler(mock_handler)

        loader = LoadConfiguration(file_path="dummy.yaml")
        self._reset_loader(loader)

        result1 = loader.load()
        result2 = loader.load()

        assert isinstance(result1, AppConfiguration)
        assert result1 is result2
        assert mock_instance.read.call_count == 1

    @patch("pricelab_retriever.adapter.outbound.configuration.load_configuration.Handler")
    def test_reload(self, mock_handler):
        mock_instance = self._mock_handler(mock_handler)

        loader = LoadConfiguration(file_path="dummy.yaml")
        self._reset_loader(loader)

        result1 = loader.load()
        result2 = loader.reload()

        assert isinstance(result1, AppConfiguration)
        assert isinstance(result2, AppConfiguration)
        assert result1 is not result2
        assert mock_instance.read.call_count == 2