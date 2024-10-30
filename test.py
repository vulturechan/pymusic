import unittest
from unittest.mock import patch, MagicMock
from your_module import Conversor

class TestConversor(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='number=0\npathsafe=/mock/path\n')
    def test_load_config(self, mock_open):
        con = Conversor()
        con.load_config()
        
        self.assertEqual(con._number, 0)
        self.assertEqual(con._pathsafe, "/mock/path")

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='http://example.com/video1\nhttp://example.com/video2\n')
    def test_load_urls(self, mock_open):
        con = Conversor()
        con.load_urls("/mock/path/to/urls.txt")
        
        self.assertEqual(len(con._urls), 2)
        self.assertEqual(con._urls[0], 'http://example.com/video1')
        self.assertEqual(con._urls[1], 'http://example.com/video2')

    @patch('pytube.YouTube')
    def test_conversorMP3(self, mock_YouTube):
        con = Conversor()
        con._pathsafe = "/mock/path"
        con._urls = ['http://example.com/video1']
        mock_video = MagicMock()
        mock_streams = MagicMock()
        mock_audio_stream = MagicMock()
        mock_YouTube.return_value = mock_video
        mock_video.streams.filter.return_value.last.return_value = mock_audio_stream
        mock_audio_stream.download.return_value = None
        con.conversorMP3()
        mock_audio_stream.download.assert_called_once()
        
    @patch('pytube.YouTube')
    def test_conversorMP4(self, mock_YouTube):
        con = Conversor()
        con._pathsafe = "/mock/path"
        con._urls = ['http://example.com/video1']
        mock_video = MagicMock()
        mock_streams = MagicMock()
        mock_YouTube.return_value = mock_video
        mock_video.streams.last.return_value = MagicMock()
        mock_video.streams.last.return_value.download.return_value = None
        con.conversorMP4()
        mock_video.streams.last.return_value.download.assert_called_once()

if __name__ == '__main__':
    unittest.main()

