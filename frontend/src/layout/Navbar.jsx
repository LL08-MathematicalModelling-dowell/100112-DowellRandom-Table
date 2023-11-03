import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import AddIcon from '@mui/icons-material/Add';

const Navbar = ({ onAddSearch }) => {
    return (
        <AppBar position='fixed'>
            <Toolbar>
                <Typography variant="h6" style={{ flexGrow: 1 }}>
                    DoWell Random
                </Typography>
                <IconButton onClick={onAddSearch}>
                    <AddIcon />
                </IconButton>
            </Toolbar>
        </AppBar>
    );
};
export default Navbar;