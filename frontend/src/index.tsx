import React, {useState} from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from './App';
import './index.css';
import axios from "axios";

import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './css/fontawesome/css/all.min.css'
import './css/mycss.css'

const container = document.getElementById('root')!;
const root = createRoot(container);

root.render(
  <Router>
    <Routes>
      <Route path="/" element={<HomePage />}></Route>
      <Route path="/login" element={<LoginPage/>}></Route>
    </Routes>
  </Router>,
);

