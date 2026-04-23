import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import data_fetcher


@pytest.mark.asyncio
async def test_get_ongoing_games_success():
    mock_data = {
        'status': 'success',
        'data': {
            'segments': [
                {
                    'team1': 'Team A',
                    'team2': 'Team B',
                    'match_page': '123',
                    'match_event': 'VCT Americas'
                }
            ]
        }
    }
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value=mock_data)
        mock_response.raise_for_status = MagicMock()
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response)

        result = await data_fetcher.get_ongoing_games()
        assert result == mock_data
        # Check filtering
        assert len(result['data']['segments']) == 1


@pytest.mark.asyncio
async def test_get_ongoing_games_no_na():
    mock_data = {
        'status': 'success',
        'data': {
            'segments': [
                {
                    'team1': 'Team A',
                    'team2': 'Team B',
                    'match_page': '123',
                    'match_event': 'VCT LATAM'  # Not NA
                }
            ]
        }
    }
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value=mock_data)
        mock_response.raise_for_status = MagicMock()
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response)

        result = await data_fetcher.get_ongoing_games()
        assert len(result['data']['segments']) == 0  # Filtered out


@pytest.mark.asyncio
async def test_get_previous_games_success():
    mock_data = {
        'status': 'success',
        'data': {
            'segments': [
                {
                    'team1': 'Team A',
                    'team2': 'Team B',
                    'date': '2026-01-01',
                    'match_page': '123'
                }
            ]
        }
    }
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value=mock_data)
        mock_response.raise_for_status = MagicMock()
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response)

        result = await data_fetcher.get_previous_games(2026)
        assert result == mock_data


@pytest.mark.asyncio
async def test_get_future_games_success():
    mock_data = {
        'status': 'success',
        'data': {
            'segments': [
                {
                    'team1': 'Team A',
                    'team2': 'Team B',
                    'match_page': '123'
                }
            ]
        }
    }
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value=mock_data)
        mock_response.raise_for_status = MagicMock()
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response)

        result = await data_fetcher.get_future_games()
        assert result == mock_data


@pytest.mark.asyncio
async def test_get_team_info_success():
    mock_data = {
        'status': 'success',
        'data': {
            'name': 'Team A',
            'roster': [{'name': 'Player1'}]
        }
    }
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value=mock_data)
        mock_response.raise_for_status = MagicMock()
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response)

        result = await data_fetcher.get_team_info('123')
        assert result == mock_data


@pytest.mark.asyncio
async def test_api_error():
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock(
            side_effect=Exception("API Error"))
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response)

        with pytest.raises(Exception):
            await data_fetcher.get_ongoing_games()


@pytest.mark.asyncio
async def test_caching():
    mock_data = {'status': 'success', 'data': {'segments': []}}
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value=mock_data)
        mock_response.raise_for_status = MagicMock()
        mock_get = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value.get = mock_get

        # First call
        result1 = await data_fetcher.get_ongoing_games()
        # Second call should use cache
        result2 = await data_fetcher.get_ongoing_games()

        assert result1 == result2
        assert mock_get.call_count == 1  # Only called once
