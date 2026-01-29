import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from app_gateway.services.assets_services import AssetDataService

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_get_all_assets_success(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{'ticker': 'AAPL'}]
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    result = await AssetDataService.get_all_assets()
    assert result == [{'ticker': 'AAPL'}]

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_get_all_assets_error(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await AssetDataService.get_all_assets()
    assert exc.value.status_code == 500

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_get_asset_by_ticker_success(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'id': '123', 'ticker': 'AAPL'}
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    result = await AssetDataService.get_asset_by_ticker('aapl')
    assert result['ticker'] == 'AAPL'

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_get_asset_by_ticker_not_found(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    result = await AssetDataService.get_asset_by_ticker('XXXX')
    assert result is None

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_get_asset_by_ticker_error(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await AssetDataService.get_asset_by_ticker('AAPL')
    assert exc.value.status_code == 500

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_create_asset_bad_request(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await AssetDataService.create_asset({'ticker': 'AAPL'})
    assert exc.value.status_code == 400

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_create_asset_internal_error(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    with pytest.raises(HTTPException) as exc:
        await AssetDataService.create_asset({'ticker': 'AAPL'})
    assert exc.value.status_code == 500

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_create_asset_success(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {'id': '123', 'ticker': 'AAPL'}
    mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
    result = await AssetDataService.create_asset({'ticker': 'AAPL'})
    assert result['ticker'] == 'AAPL'