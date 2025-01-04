import React, { useState } from 'react';
import { Box, Button, TextField, MenuItem, Grid, FormControl, InputLabel, Select, Chip, Typography, Divider, Checkbox, FormControlLabel, Alert, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Enum values from the backend
const SEX_OPTIONS = ["male", "female"];
const RACE_OPTIONS = ["asian", "black", "hispanic", "white", "other"];
const CONTINENT_OPTIONS = ["north_america", "south_america", "europe", "asia", "africa", "oceania", "antarctica"];
const ATHLETICISM_OPTIONS = ["sedentary", "light", "moderate", "very_active", "athlete"];
const DIET_OPTIONS = ["omnivore", "vegetarian", "vegan", "pescatarian", "keto", "other"];
const PREEXISTING_CONDITIONS = [
  "cancer", "cardiovascular_diseases", "diabetes", "obesity_metabolic_syndrome",
  "neurological_disorders", "autoimmune_conditions", "respiratory_diseases",
  "chronic_kidney_disease", "gastrointestinal_disorders", "mental_health_disorders",
  "substance_dependency"
];
const PRIOR_CONDITIONS = [
  "cancer_remission", "cardiovascular_resolved", "diabetes_resolved",
  "neurological_resolved", "respiratory_resolved", "mental_health_resolved",
  "infectious_resolved"
];
const SURGERIES = [
  "cancer_related", "cardiac", "orthopedic", "neurological",
  "bariatric", "gynecological", "transplantation"
];
const MEDICATIONS = [
  "cancer_therapies", "cardiac_drugs", "antihypertensives", "diabetes_medication",
  "neurological_drugs", "psychiatric_medications", "pain_management",
  "nutritional_supplements"
];

const ProfileForm = ({ onProfileSubmit, onMatchResults }) => {
  const [formData, setFormData] = useState({
    physical: {
      age: '',
      weight: '',
      height: '',
      sex: 'male'
    },
    demographics: {
      race: 'white',
      location: 'north_america'
    },
    medical_history: {
      preexisting_conditions: [],
      prior_conditions: [],
      surgeries: [],
      active_medications: []
    },
    lifestyle: {
      athleticism: 'moderate',
      diet: 'omnivore'
    }
  });
  const [username, setUsername] = useState('');
  const [saveProfile, setSaveProfile] = useState(false);
  const [saveUsername, setSaveUsername] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  const handleLoadProfile = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/profiles/${username}`);
      if (!response.ok) {
        throw new Error('Profile not found');
      }
      const data = await response.json();
      setFormData(data.profile);
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
      const response = await fetch(`${API_BASE_URL}/profiles/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: saveUsername,
          profile: formData
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save profile');
      }

      setMessage('Profile loaded successfully');
      setError('');
      setSaveProfile(false);
      setSaveUsername('');
    } catch (err) {
      setError('Failed to save profile: ' + err.message);
      setMessage('');
    }
  };

  const handleDeleteProfile = async () => {
    if (!saveUsername) {
      setError('Please enter a username to delete');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/profiles/${saveUsername}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        // Check if profile not found
        if (response.status === 404) {
          setError('No profile found with this username');
          return;
        }
        throw new Error('Could not delete profile');
      }

      setMessage('Profile deleted successfully');
      setError('');
      setSaveProfile(false);
      setSaveUsername('');
      setDeleteDialogOpen(false);
    } catch (err) {
      setError(err.message);
      setMessage('');
    }
  };

  const handleDeleteClick = async () => {
    // First check if profile exists
    try {
      const response = await fetch(`${API_BASE_URL}/profiles/${saveUsername}`);
      if (!response.ok) {
        setError('No profile found with this username');
        return;
      }
      // If profile exists, show confirmation dialog
      setDeleteDialogOpen(true);
    } catch (err) {
      setError('Could not verify profile existence');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Convert string values to numbers where needed
      const formattedProfile = {
        ...formData,
        physical: {
          ...formData.physical,
          age: parseInt(formData.physical.age),
          weight: parseFloat(formData.physical.weight),
          height: parseFloat(formData.physical.height)
        }
      };
      
      onProfileSubmit(formattedProfile);
      const response = await axios.post(`${API_BASE_URL}/match/`, formattedProfile);
      onMatchResults(response.data);
    } catch (error) {
      console.error('Error matching profile:', error);
    }
  };

  const handleChange = (section, field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: event.target.value
      }
    }));
  };

  const handleMultiSelect = (section, field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: event.target.value
      }
    }));
  };

  const DeleteConfirmationDialog = () => (
    <Dialog 
      open={deleteDialogOpen} 
      onClose={() => setDeleteDialogOpen(false)}
      PaperProps={{
        sx: {
          borderRadius: '8px',
          padding: '8px'
        }
      }}
    >
      <DialogTitle sx={{ 
        fontSize: '1.25rem',
        fontWeight: 400,
        pb: 1,
        fontFamily: '"Roboto","Helvetica","Arial",sans-serif'
      }}>
        Confirm Delete
      </DialogTitle>
      <DialogContent sx={{ 
        pb: 2,
        fontFamily: '"Roboto","Helvetica","Arial",sans-serif',
        fontSize: '1rem',
        color: 'rgba(0, 0, 0, 0.87)'
      }}>
        Are you sure you want to delete the profile for "{saveUsername}"?
      </DialogContent>
      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button 
          onClick={() => setDeleteDialogOpen(false)}
          variant="text"
          sx={{ 
            color: 'primary.main',
            textTransform: 'none',
            fontWeight: 500
          }}
        >
          Cancel
        </Button>
        <Button 
          onClick={handleDeleteProfile}
          variant="text"
          color="error"
          sx={{ 
            textTransform: 'none',
            fontWeight: 500
          }}
        >
          Delete
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <Box>
      {/* Load Profile Section */}
      <Box sx={{ mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                label="Enter Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                size="small"
                sx={{ flex: 1 }}
              />
              <Button 
                variant="contained" 
                onClick={handleLoadProfile}
                disabled={!username}
              >
                Load Profile
              </Button>
            </Box>
            {/* Error message for load profile */}
            {error && error.includes('not found') && (
              <Alert severity="error" sx={{ mt: 1 }}>
                {error}
              </Alert>
            )}
          </Box>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', my: 2 }}>
          <Divider sx={{ flex: 1 }} />
          <Typography sx={{ mx: 2 }}>OR</Typography>
          <Divider sx={{ flex: 1 }} />
        </Box>
      </Box>

      <Grid container spacing={2}>
        {/* Physical Characteristics */}
        <Grid item xs={12}>
          <Typography variant="h6">Physical Characteristics</Typography>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            required
            label="Age"
            type="number"
            value={formData.physical.age}
            onChange={handleChange('physical', 'age')}
            inputProps={{ min: 0, max: 120 }}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            required
            label="Weight (lbs)"
            type="number"
            value={formData.physical.weight}
            onChange={handleChange('physical', 'weight')}
            inputProps={{ min: 0, max: 1000 }}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            required
            label="Height (inches)"
            type="number"
            value={formData.physical.height}
            onChange={handleChange('physical', 'height')}
            inputProps={{ min: 0, max: 120 }}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth required>
            <InputLabel>Sex</InputLabel>
            <Select
              value={formData.physical.sex}
              onChange={handleChange('physical', 'sex')}
              label="Sex"
            >
              {SEX_OPTIONS.map(option => (
                <MenuItem key={option} value={option}>
                  {option.charAt(0).toUpperCase() + option.slice(1)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        {/* Demographics */}
        <Grid item xs={12}>
          <Typography variant="h6">Demographics</Typography>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth required>
            <InputLabel>Race</InputLabel>
            <Select
              value={formData.demographics.race}
              onChange={handleChange('demographics', 'race')}
              label="Race"
            >
              {RACE_OPTIONS.map(option => (
                <MenuItem key={option} value={option}>
                  {option.charAt(0).toUpperCase() + option.slice(1)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth required>
            <InputLabel>Location</InputLabel>
            <Select
              value={formData.demographics.location}
              onChange={handleChange('demographics', 'location')}
              label="Location"
            >
              {CONTINENT_OPTIONS.map(option => (
                <MenuItem key={option} value={option}>
                  {option.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        {/* Medical History */}
        <Grid item xs={12}>
          <Typography variant="h6">Medical History</Typography>
        </Grid>
        
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Preexisting Conditions</InputLabel>
            <Select
              multiple
              value={formData.medical_history.preexisting_conditions}
              onChange={handleMultiSelect('medical_history', 'preexisting_conditions')}
              label="Preexisting Conditions"
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip key={value} label={value.split('_').join(' ')} />
                  ))}
                </Box>
              )}
            >
              {PREEXISTING_CONDITIONS.map(option => (
                <MenuItem key={option} value={option}>
                  {option.split('_').join(' ')}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Prior Conditions</InputLabel>
            <Select
              multiple
              value={formData.medical_history.prior_conditions}
              onChange={handleMultiSelect('medical_history', 'prior_conditions')}
              label="Prior Conditions"
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip key={value} label={value.split('_').join(' ')} />
                  ))}
                </Box>
              )}
            >
              {PRIOR_CONDITIONS.map(option => (
                <MenuItem key={option} value={option}>
                  {option.split('_').join(' ')}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Surgeries</InputLabel>
            <Select
              multiple
              value={formData.medical_history.surgeries}
              onChange={handleMultiSelect('medical_history', 'surgeries')}
              label="Surgeries"
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip key={value} label={value.split('_').join(' ')} />
                  ))}
                </Box>
              )}
            >
              {SURGERIES.map(option => (
                <MenuItem key={option} value={option}>
                  {option.split('_').join(' ')}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Active Medications</InputLabel>
            <Select
              multiple
              value={formData.medical_history.active_medications}
              onChange={handleMultiSelect('medical_history', 'active_medications')}
              label="Active Medications"
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip key={value} label={value.split('_').join(' ')} />
                  ))}
                </Box>
              )}
            >
              {MEDICATIONS.map(option => (
                <MenuItem key={option} value={option}>
                  {option.split('_').join(' ')}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        {/* Lifestyle */}
        <Grid item xs={12}>
          <Typography variant="h6">Lifestyle</Typography>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth required>
            <InputLabel>Athleticism</InputLabel>
            <Select
              value={formData.lifestyle.athleticism}
              onChange={handleChange('lifestyle', 'athleticism')}
              label="Athleticism"
            >
              {ATHLETICISM_OPTIONS.map(option => (
                <MenuItem key={option} value={option}>
                  {option.split('_').join(' ')}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth required>
            <InputLabel>Diet</InputLabel>
            <Select
              value={formData.lifestyle.diet}
              onChange={handleChange('lifestyle', 'diet')}
              label="Diet"
            >
              {DIET_OPTIONS.map(option => (
                <MenuItem key={option} value={option}>
                  {option.charAt(0).toUpperCase() + option.slice(1)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      {/* Save Profile and Match Section */}
      <Box sx={{ mt: 4, mb: 2 }}>
        {/* Save Profile Row */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <FormControlLabel
            control={
              <Checkbox
                checked={saveProfile}
                onChange={(e) => setSaveProfile(e.target.checked)}
              />
            }
            label="Save this profile"
            sx={{ m: 0 }}
          />
          
          {saveProfile && (
            <>
              <TextField
                label="Choose Username"
                value={saveUsername}
                onChange={(e) => setSaveUsername(e.target.value)}
                size="small"
                sx={{ width: '300px' }}
              />
              <Button 
                variant="contained"
                onClick={handleSaveProfile}
                sx={{ minWidth: '120px' }}
              >
                Save Profile
              </Button>
              <Button 
                variant="outlined"
                color="error"
                onClick={handleDeleteClick}
                sx={{ minWidth: '120px' }}
              >
                Delete Profile
              </Button>
            </>
          )}
        </Box>

        {/* Add confirmation dialog */}
        <DeleteConfirmationDialog />

        {/* Messages */}
        {error && !error.includes('not found') && (
          <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
        )}
        {message && (
          <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>
        )}

        {/* Match Profile Button - Separate Row */}
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleSubmit}
          fullWidth
        >
          Match Profile
        </Button>
      </Box>
    </Box>
  );
};

export default ProfileForm; 