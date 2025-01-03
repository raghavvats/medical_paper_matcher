import React, { useState } from 'react';
import { Box, Button, TextField, MenuItem, Grid, FormControl, InputLabel, Select, Chip, Typography } from '@mui/material';
import axios from 'axios';

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
  const [profile, setProfile] = useState({
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Convert string values to numbers where needed
      const formattedProfile = {
        ...profile,
        physical: {
          ...profile.physical,
          age: parseInt(profile.physical.age),
          weight: parseFloat(profile.physical.weight),
          height: parseFloat(profile.physical.height)
        }
      };
      
      onProfileSubmit(formattedProfile);
      const response = await axios.post('http://localhost:8000/match/', formattedProfile);
      onMatchResults(response.data);
    } catch (error) {
      console.error('Error matching profile:', error);
    }
  };

  const handleChange = (section, field) => (event) => {
    setProfile(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: event.target.value
      }
    }));
  };

  const handleMultiSelect = (section, field) => (event) => {
    setProfile(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: event.target.value
      }
    }));
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
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
            value={profile.physical.age}
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
            value={profile.physical.weight}
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
            value={profile.physical.height}
            onChange={handleChange('physical', 'height')}
            inputProps={{ min: 0, max: 120 }}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth required>
            <InputLabel>Sex</InputLabel>
            <Select
              value={profile.physical.sex}
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
              value={profile.demographics.race}
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
              value={profile.demographics.location}
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
              value={profile.medical_history.preexisting_conditions}
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
              value={profile.medical_history.prior_conditions}
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
              value={profile.medical_history.surgeries}
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
              value={profile.medical_history.active_medications}
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
              value={profile.lifestyle.athleticism}
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
              value={profile.lifestyle.diet}
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

        <Grid item xs={12}>
          <Button 
            variant="contained" 
            color="primary" 
            type="submit"
            fullWidth
            size="large"
            sx={{ mt: 2 }}
          >
            Match Profile
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProfileForm; 