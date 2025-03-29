import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Select,
  MenuItem,
  Button,
  FormControl,
  InputLabel,
  Grid,
  Paper,
  IconButton,
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [voices, setVoices] = useState({});
  const [characters, setCharacters] = useState([
    { id: 1, name: 'Character_A', text: '', voice: '' },
    { id: 2, name: 'Character_B', text: '', voice: '' },
    { id: 3, name: 'Character_C', text: '', voice: '' },
  ]);
  const [language, setLanguage] = useState('en-US');
  const [speed, setSpeed] = useState(1.0);

  useEffect(() => {
    fetchVoices();
  }, []);

  const fetchVoices = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/voices`);
      setVoices(response.data);
    } catch (error) {
      console.error('Error fetching voices:', error);
    }
  };

  const handleTextChange = (id, value) => {
    setCharacters(characters.map(char =>
      char.id === id ? { ...char, text: value } : char
    ));
  };

  const handleVoiceChange = (id, value) => {
    setCharacters(characters.map(char =>
      char.id === id ? { ...char, voice: value } : char
    ));
  };

  const handlePlay = async (character) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/synthesize`,
        {
          text: character.text,
          voice: character.voice,
        },
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const audio = new Audio(url);
      audio.play();
    } catch (error) {
      console.error('Error synthesizing speech:', error);
    }
  };

  const addCharacter = () => {
    const newId = Math.max(...characters.map(c => c.id)) + 1;
    setCharacters([...characters, {
      id: newId,
      name: `Character_${newId}`,
      text: '',
      voice: ''
    }]);
  };

  const removeCharacter = (id) => {
    setCharacters(characters.filter(char => char.id !== id));
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          多角色文本配音工具
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>语言</InputLabel>
                <Select
                  value={language}
                  label="语言"
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  <MenuItem value="en-US">英语 (English)</MenuItem>
                  <MenuItem value="es-ES">西班牙语 (Español)</MenuItem>
                  <MenuItem value="pt-PT">葡萄牙语 (Português)</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>语速</InputLabel>
                <Select
                  value={speed}
                  label="语速"
                  onChange={(e) => setSpeed(e.target.value)}
                >
                  <MenuItem value={0.5}>0.5x</MenuItem>
                  <MenuItem value={0.75}>0.75x</MenuItem>
                  <MenuItem value={1.0}>1.0x</MenuItem>
                  <MenuItem value={1.25}>1.25x</MenuItem>
                  <MenuItem value={1.5}>1.5x</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Paper>

        {characters.map((character) => (
          <Paper key={character.id} sx={{ p: 3, mb: 2 }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={2}>
                <Typography variant="subtitle1">{character.name}</Typography>
              </Grid>
              <Grid item xs={4}>
                <FormControl fullWidth>
                  <InputLabel>声音</InputLabel>
                  <Select
                    value={character.voice}
                    label="声音"
                    onChange={(e) => handleVoiceChange(character.id, e.target.value)}
                  >
                    {voices[language]?.map((voice) => (
                      <MenuItem key={voice.name} value={voice.name}>
                        {voice.name} ({voice.gender})
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={4}>
                <TextField
                  fullWidth
                  label="文本"
                  multiline
                  rows={2}
                  value={character.text}
                  onChange={(e) => handleTextChange(character.id, e.target.value)}
                />
              </Grid>
              <Grid item xs={2}>
                <IconButton
                  color="primary"
                  onClick={() => handlePlay(character)}
                  disabled={!character.text || !character.voice}
                >
                  <PlayArrowIcon />
                </IconButton>
                <IconButton
                  color="error"
                  onClick={() => removeCharacter(character.id)}
                >
                  <DeleteIcon />
                </IconButton>
              </Grid>
            </Grid>
          </Paper>
        ))}

        <Button
          variant="contained"
          color="primary"
          onClick={addCharacter}
          sx={{ mt: 2 }}
        >
          添加新角色
        </Button>
      </Box>
    </Container>
  );
}

export default App; 