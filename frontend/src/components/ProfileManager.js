import React, { useState } from 'react';
import { TextField, Button, Checkbox, FormControlLabel, Box, Typography, Alert, Paper } from '@mui/material';

const ProfileManager = ({ onLoadProfile, currentProfile }) => {
    const [username, setUsername] = useState('');
    const [saveProfile, setSaveProfile] = useState(false);
    const [saveUsername, setSaveUsername] = useState('');
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');

    const handleLoadProfile = async () => {
        try {
            const response = await fetch(`/api/profiles/${username}`);
            if (!response.ok) {
                throw new Error('Profile not found');
            }
            const data = await response.json();
            onLoadProfile(data.profile);
            setMessage('Profile loaded successfully');
            setError('');
        } catch (err) {
            setError('Failed to load profile: ' + err.message);
            setMessage('');
        }
    };

    const handleSaveProfile = async () => {
        if (!saveUsername) {
            setError('Please enter a username to save the profile');
            return;
        }

        try {
            const response = await fetch('/api/profiles/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: saveUsername,
                    profile: currentProfile
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to save profile');
            }

            setMessage('Profile saved successfully');
            setError('');
            setSaveProfile(false);
            setSaveUsername('');
        } catch (err) {
            setError('Failed to save profile: ' + err.message);
            setMessage('');
        }
    };

    return (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
                Profile Management
            </Typography>
            
            {/* Load Profile Section */}
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <TextField
                    label="Load Profile Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    size="small"
                    sx={{ backgroundColor: '#fff' }}
                />
                <Button 
                    variant="contained" 
                    onClick={handleLoadProfile}
                    disabled={!username}
                >
                    Load Profile
                </Button>
            </Box>

            {/* Save Profile Section */}
            <Box sx={{ mb: 2 }}>
                <FormControlLabel
                    control={
                        <Checkbox
                            checked={saveProfile}
                            onChange={(e) => setSaveProfile(e.target.checked)}
                        />
                    }
                    label="Save this profile"
                />
                
                {saveProfile && (
                    <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
                        <TextField
                            label="Save Profile Username"
                            value={saveUsername}
                            onChange={(e) => setSaveUsername(e.target.value)}
                            size="small"
                            sx={{ backgroundColor: '#fff' }}
                        />
                        <Button 
                            variant="contained" 
                            onClick={handleSaveProfile}
                            disabled={!saveUsername || !currentProfile}
                        >
                            Save Profile
                        </Button>
                    </Box>
                )}
            </Box>

            {/* Messages */}
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
            {message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}
        </Paper>
    );
};

export default ProfileManager; 