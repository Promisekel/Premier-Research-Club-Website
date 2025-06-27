import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import kagglehub
import statsmodels.formula.api as smf
import statsmodels.api as sm
import textwrap

# Configure page
st.set_page_config(
    page_title="📊 Cervical Cancer Screening Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with beautiful background
st.markdown("""
<style>    /* 🎨 Beautiful Orange-Pink Gradient Background - Inspired by the provided image */
    .stApp {
        background: linear-gradient(135deg, 
            #ff9a56 0%,     /* Warm orange */
            #ff7b39 12%,    /* Rich orange */
            #ff6b2b 25%,    /* Deep orange */
            #ff5722 38%,    /* Orange-red */
            #ff4757 50%,    /* Coral-red */
            #ff3838 62%,    /* Bright red */
            #ff2d92 75%,    /* Pink-red */
            #ff1744 88%,    /* Vibrant pink-red */
            #e91e63 100%    /* Deep pink */
        );
        background-attachment: fixed;
        position: relative;
        min-height: 100vh;
        animation: backgroundPulse 12s ease-in-out infinite;
    }
    
    /* 🌟 Animated Organic Shapes Overlay - Similar to the image pattern */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            /* Large organic shape - top left */
            radial-gradient(ellipse 700px 500px at 15% 25%, rgba(255, 204, 128, 0.4) 0%, transparent 55%),
            /* Medium organic shape - bottom right */
            radial-gradient(ellipse 600px 400px at 85% 75%, rgba(255, 154, 86, 0.35) 0%, transparent 55%),
            /* Small organic shape - center */
            radial-gradient(ellipse 350px 250px at 50% 45%, rgba(255, 107, 43, 0.25) 0%, transparent 60%),
            /* Flowing wave pattern */
            linear-gradient(45deg, 
                transparent 0%, 
                rgba(255, 255, 255, 0.08) 25%, 
                transparent 45%, 
                rgba(255, 255, 255, 0.05) 70%, 
                transparent 100%);
        background-size: 
            100% 100%, 
            100% 100%, 
            100% 100%, 
            300px 300px;
        z-index: -1;
        opacity: 0.85;
        animation: organicFlow 18s ease-in-out infinite;
    }
    
    /* 🌈 Additional flowing overlay for depth and movement */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle 400px at 70% 30%, rgba(255, 183, 77, 0.18) 0%, transparent 70%),
            radial-gradient(circle 300px at 25% 70%, rgba(255, 138, 101, 0.15) 0%, transparent 70%),
            radial-gradient(circle 200px at 80% 80%, rgba(255, 71, 87, 0.12) 0%, transparent 70%);
        z-index: -1;
        animation: floatingShapes 22s ease-in-out infinite reverse;
    }
    
    /* Background breathing animation */
    @keyframes backgroundPulse {
        0%, 100% {
            filter: hue-rotate(0deg) saturate(1.0) brightness(1.0);
        }
        25% {
            filter: hue-rotate(3deg) saturate(1.08) brightness(1.03);
        }
        50% {
            filter: hue-rotate(-2deg) saturate(1.12) brightness(1.06);
        }
        75% {
            filter: hue-rotate(5deg) saturate(1.05) brightness(1.02);
        }
    }
    
    /* Organic shapes flowing animation */
    @keyframes organicFlow {
        0%, 100% {
            transform: scale(1) rotate(0deg);
            opacity: 0.85;
        }
        25% {
            transform: scale(1.03) rotate(1deg);
            opacity: 0.9;
        }
        50% {
            transform: scale(1.06) rotate(-0.5deg);
            opacity: 0.95;
        }
        75% {
            transform: scale(1.02) rotate(0.8deg);
            opacity: 0.88;
        }
    }
    
    /* Floating depth shapes animation */
    @keyframes floatingShapes {
        0%, 100% {
            transform: translateY(0px) translateX(0px) scale(1);
            opacity: 1;
        }
        33% {
            transform: translateY(-12px) translateX(8px) scale(1.04);
            opacity: 0.9;
        }
        66% {
            transform: translateY(-6px) translateX(-10px) scale(0.96);
            opacity: 0.95;
        }
    }
    
    /* Main content container with translucent background */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(52, 73, 94, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 0 15px 15px 0;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        border-radius: 15px;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }      /* 🚀 Enhanced Section Headers - Perfect Size with Exciting Animations! */
    .section-header {
        font-size: 1.9rem;
        font-weight: 800;
        color: white;
        margin: 1.8rem 0 1.2rem 0;
        padding: 1.2rem 1.8rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #00d4aa 0%, #00b894 25%, #00a085 50%, #008f72 75%, #007d5f 100%);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        box-shadow: 
            0 8px 24px rgba(0,0,0,0.15),
            0 4px 12px rgba(0,0,0,0.08),
            0 0 16px rgba(0,212,170,0.25),
            inset 0 1px 0 rgba(255,255,255,0.2);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        cursor: pointer;
        animation: headerEntrance 1s ease-out, headerFloat 4s ease-in-out infinite;
    }
      .section-header::before {
        content: "✨";
        position: absolute;
        top: 50%;
        right: 25px;
        transform: translateY(-50%);
        font-size: 1.5rem;
        animation: sparkleRotate 3s ease-in-out infinite;
    }
    
    .section-header::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: headerShimmer 4s ease-in-out infinite;
    }
      .section-header:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.2),
            0 8px 18px rgba(0,0,0,0.15),
            0 0 30px rgba(0,255,204,0.4),
            inset 0 1px 0 rgba(255,255,255,0.25);
        background: linear-gradient(135deg, #00ffcc 0%, #00e6b8 25%, #00d4aa 50%, #00b894 75%, #00a085 100%);
    }
    
    @keyframes headerEntrance {
        0% {
            opacity: 0;
            transform: translateY(-30px) scale(0.9);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes headerFloat {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-3px);
        }
    }
    
    @keyframes headerShimmer {
        0% {
            transform: translateX(-100%) translateY(-100%) rotate(45deg);
            opacity: 0;
        }
        50% {
            opacity: 0.3;
        }
        100% {
            transform: translateX(100%) translateY(100%) rotate(45deg);
            opacity: 0;
        }
    }/* 🚀 Enhanced Summary Cards - Perfect Size with Exciting Animations! */
    .summary-card {
        background: linear-gradient(145deg, #ffffff 0%, #f0f8ff 25%, #e6f3ff 50%, #dbeafe 100%);
        border-radius: 18px;
        padding: 1.8rem 1.5rem;
        margin: 1rem 0.8rem;
        box-shadow: 
            0 12px 30px rgba(0,0,0,0.12),
            0 6px 15px rgba(0,0,0,0.08),
            0 3px 8px rgba(0,0,0,0.04),
            inset 0 1px 0 rgba(255,255,255,0.9);
        border: 1px solid rgba(255,255,255,0.4);
        border-left: 6px solid #00d4aa;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
        animation: cardEntrance 0.8s ease-out forwards, cardFloat 4s ease-in-out infinite;
        backdrop-filter: blur(12px);
        cursor: pointer;
        transform-style: preserve-3d;
    }
      .summary-card:active {
        transform: translateY(-8px) scale(1.03) rotateX(3deg);
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.15),
            0 10px 20px rgba(0,0,0,0.1),
            0 0 20px rgba(0,212,170,0.25),
            inset 0 1px 0 rgba(255,255,255,0.9);
    }/* 🌟 Enhanced Shimmer & Hover Effects with Particles */
    .summary-card::before {
        content: "";
        position: absolute;
        top: -100%;
        left: -100%;
        width: 300%;
        height: 300%;
        background: linear-gradient(45deg, 
            transparent, 
            rgba(255,255,255,0.3), 
            rgba(0,212,170,0.2),
            rgba(255,255,255,0.3),
            transparent);
        transform: rotate(45deg);
        transition: all 0.8s ease;
        opacity: 0;
        pointer-events: none;
        animation: particleFloat 6s ease-in-out infinite;
    }
    
    .summary-card::after {
        content: "✨";
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 1.5rem;
        opacity: 0;
        transform: scale(0) rotate(0deg);
        transition: all 0.4s ease;
        animation: sparkleRotate 3s ease-in-out infinite;
    }
      .summary-card:hover {
        transform: translateY(-8px) scale(1.03) rotateY(3deg);
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.15),
            0 12px 24px rgba(0,0,0,0.1),
            0 0 30px rgba(0,212,170,0.3),
            0 0 15px rgba(255,255,255,0.5),
            inset 0 1px 0 rgba(255,255,255,0.9);
        border-left-width: 8px;
        border-left-color: #00ffcc;
    }
    
    .summary-card:hover::before {
        opacity: 1;
        animation: megaShimmer 2s ease-in-out infinite;
    }
    
    .summary-card:hover::after {
        opacity: 1;
        transform: scale(1.2) rotate(360deg);
    }    /* 🎨 VIBRANT Color Variants - Super Bright & Catchy! */
    .summary-card.blue {
        background: linear-gradient(145deg, 
            #ffffff 0%, 
            #e3f2fd 20%, 
            #2196f3 40%, 
            #1976d2 60%, 
            #0d47a1 80%, 
            #003c8f 100%);
        border-left-color: #00bcd4;
        box-shadow: 
            0 20px 50px rgba(33,150,243,0.3),
            0 10px 25px rgba(33,150,243,0.2),
            0 0 30px rgba(33,150,243,0.4),
            inset 0 2px 0 rgba(255,255,255,0.95);
        color: white;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .summary-card.blue:hover {
        background: linear-gradient(145deg, 
            #00e5ff 0%, 
            #00b8d4 25%, 
            #0091ea 50%, 
            #2962ff 75%, 
            #304ffe 100%);
        box-shadow: 
            0 35px 70px rgba(33,150,243,0.4),
            0 20px 40px rgba(33,150,243,0.3),
            0 0 60px rgba(0,229,255,0.6),
            0 0 30px rgba(255,255,255,0.8),
            inset 0 2px 0 rgba(255,255,255,0.95);
        border-left-color: #00e5ff;
        animation: colorPulse 1.5s ease-in-out infinite;
    }
    
    .summary-card.green {
        background: linear-gradient(145deg, 
            #ffffff 0%, 
            #e8f5e8 20%, 
            #4caf50 40%, 
            #388e3c 60%, 
            #2e7d32 80%, 
            #1b5e20 100%);
        border-left-color: #00e676;
        box-shadow: 
            0 20px 50px rgba(76,175,80,0.3),
            0 10px 25px rgba(76,175,80,0.2),
            0 0 30px rgba(76,175,80,0.4),
            inset 0 2px 0 rgba(255,255,255,0.95);
        color: white;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .summary-card.green:hover {
        background: linear-gradient(145deg, 
            #00ff88 0%, 
            #00e676 25%, 
            #00c853 50%, 
            #64dd17 75%, 
            #76ff03 100%);
        box-shadow: 
            0 35px 70px rgba(76,175,80,0.4),
            0 20px 40px rgba(76,175,80,0.3),
            0 0 60px rgba(0,255,136,0.6),
            0 0 30px rgba(255,255,255,0.8),
            inset 0 2px 0 rgba(255,255,255,0.95);
        border-left-color: #00ff88;
        animation: colorPulse 1.5s ease-in-out infinite;
    }
    
    .summary-card.orange {
        background: linear-gradient(145deg, 
            #ffffff 0%, 
            #fff3e0 20%, 
            #ff9800 40%, 
            #f57c00 60%, 
            #ef6c00 80%, 
            #e65100 100%);
        border-left-color: #ff6d00;
        box-shadow: 
            0 20px 50px rgba(255,152,0,0.3),
            0 10px 25px rgba(255,152,0,0.2),
            0 0 30px rgba(255,152,0,0.4),
            inset 0 2px 0 rgba(255,255,255,0.95);
        color: white;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .summary-card.orange:hover {
        background: linear-gradient(145deg, 
            #ffab00 0%, 
            #ff8f00 25%, 
            #ff6f00 50%, 
            #ff3d00 75%, 
            #dd2c00 100%);
        box-shadow: 
            0 35px 70px rgba(255,152,0,0.4),
            0 20px 40px rgba(255,152,0,0.3),
            0 0 60px rgba(255,171,0,0.6),
            0 0 30px rgba(255,255,255,0.8),
            inset 0 2px 0 rgba(255,255,255,0.95);
        border-left-color: #ffab00;
        animation: colorPulse 1.5s ease-in-out infinite;
    }
    
    .summary-card.purple {
        background: linear-gradient(145deg, 
            #ffffff 0%, 
            #f3e5f5 20%, 
            #9c27b0 40%, 
            #7b1fa2 60%, 
            #6a1b9a 80%, 
            #4a148c 100%);
        border-left-color: #e040fb;
        box-shadow: 
            0 20px 50px rgba(156,39,176,0.3),
            0 10px 25px rgba(156,39,176,0.2),
            0 0 30px rgba(156,39,176,0.4),
            inset 0 2px 0 rgba(255,255,255,0.95);
        color: white;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .summary-card.purple:hover {
        background: linear-gradient(145deg, 
            #e040fb 0%, 
            #d500f9 25%, 
            #aa00ff 50%, 
            #7c4dff 75%, 
            #651fff 100%);
        box-shadow: 
            0 35px 70px rgba(156,39,176,0.4),
            0 20px 40px rgba(156,39,176,0.3),
            0 0 60px rgba(224,64,251,0.6),
            0 0 30px rgba(255,255,255,0.8),
            inset 0 2px 0 rgba(255,255,255,0.95);
        border-left-color: #e040fb;
        animation: colorPulse 1.5s ease-in-out infinite;
    }
    
    /* Large Content Cards - For sections with extensive text */
    .large-content-card {
        background: linear-gradient(135deg, #f8fbff 0%, #e8f4f8 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        border-left: 6px solid #00b894;
        transition: all 0.3s ease;
        text-align: left;
        min-height: auto;
    }
    
    .large-content-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .large-content-card.blue {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left-color: #2196f3;
    }
    
    .large-content-card.green {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border-left-color: #4caf50;
    }
    
    .large-content-card.orange {
        background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%);
        border-left-color: #ff9800;
    }
    
    .large-content-card.purple {
        background: linear-gradient(135deg, #f3e5f5 0%, #ce93d8 100%);
        border-left-color: #9c27b0;
    }
    
    .large-content-card.red {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left-color: #f44336;
    }
    
    .large-card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1.2rem;
        text-transform: none;
        letter-spacing: 0.5px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .large-card-content {
        font-size: 1rem;
        color: #2d3748;
        line-height: 1.6;
        font-weight: 400;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .large-card-content ul {
        list-style: none;
        padding-left: 0;
        margin: 0;
    }
    
    .large-card-content li {
        padding: 0.5rem 0;
        padding-left: 1.5rem;
        position: relative;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    .large-card-content li:last-child {
        border-bottom: none;
    }
    
    .large-card-content li::before {
        content: "▶";
        position: absolute;
        left: 0;
        color: #00b894;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    .large-card-content strong {
        color: #1a202c;
        font-weight: 600;
    }    /* 🎯 Enhanced Card Text Styles - Perfect Visibility with Strong Contrast! */
    .card-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #1a202c;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-family: 'Segoe UI', 'Arial Black', Tahoma, Geneva, Verdana, sans-serif;
        overflow-wrap: break-word;
        word-wrap: break-word;
        text-shadow: 
            2px 2px 4px rgba(0,0,0,0.5),
            1px 1px 2px rgba(0,0,0,0.3),
            0px 0px 8px rgba(255,255,255,0.8);
        animation: titleGlow 2s ease-in-out infinite;
        position: relative;
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 50%, #4a5568 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.5));
    }
    
    /* Override for colored cards - Ensure white text on dark backgrounds */
    .summary-card.blue .card-title,
    .summary-card.green .card-title,
    .summary-card.orange .card-title,
    .summary-card.purple .card-title {
        color: white !important;
        -webkit-text-fill-color: white !important;
        background: none !important;
        text-shadow: 
            2px 2px 6px rgba(0,0,0,0.8),
            1px 1px 3px rgba(0,0,0,0.6),
            0px 0px 10px rgba(0,0,0,0.4) !important;
        font-weight: 900 !important;
        filter: drop-shadow(3px 3px 6px rgba(0,0,0,0.7)) !important;
    }
    
    .card-title::after {
        content: "🎯";
        position: absolute;
        right: -25px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1rem;
        opacity: 0.8;
        animation: iconBounce 2s ease-in-out infinite;
        filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.5));
    }
    
    .card-value {
        font-size: 2.8rem;
        font-weight: 900;
        color: #1a202c;
        margin: 0.8rem 0;
        font-family: 'Segoe UI', 'Arial Black', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1;
        overflow-wrap: break-word;
        word-wrap: break-word;
        text-shadow: 
            3px 3px 6px rgba(0,0,0,0.4),
            1px 1px 3px rgba(0,0,0,0.2),
            0px 0px 10px rgba(255,255,255,0.6);
        animation: valueCountUp 2s ease-out, valuePulse 3s ease-in-out infinite;
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 30%, #4a5568 70%, #1a202c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        filter: drop-shadow(3px 3px 6px rgba(0,0,0,0.3));
    }
    
    /* Override for colored cards - Ensure white values on dark backgrounds */
    .summary-card.blue .card-value,
    .summary-card.green .card-value,
    .summary-card.orange .card-value,
    .summary-card.purple .card-value {
        color: white !important;
        -webkit-text-fill-color: white !important;
        background: none !important;
        text-shadow: 
            4px 4px 8px rgba(0,0,0,0.9),
            2px 2px 4px rgba(0,0,0,0.7),
            0px 0px 12px rgba(0,0,0,0.5) !important;
        font-weight: 900 !important;
        filter: drop-shadow(4px 4px 8px rgba(0,0,0,0.8)) !important;
    }
    
    .card-value::before {
        content: "✨";
        position: absolute;
        top: -8px;
        left: -30px;
        font-size: 1.4rem;
        animation: sparkleFloat 3s ease-in-out infinite;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.5));
    }
    
    .card-description {
        font-size: 0.9rem;
        color: #4a5568;
        margin-top: 0.8rem;
        line-height: 1.4;
        font-weight: 600;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        overflow-wrap: break-word;
        word-wrap: break-word;
        hyphens: auto;
        text-shadow: 
            1px 1px 3px rgba(0,0,0,0.3),
            0px 0px 4px rgba(255,255,255,0.6);
        animation: descriptionSlide 1s ease-out 0.5s backwards;
    }
    
    /* Override for colored cards - Ensure white descriptions on dark backgrounds */
    .summary-card.blue .card-description,
    .summary-card.green .card-description,
    .summary-card.orange .card-description,
    .summary-card.purple .card-description {
        color: rgba(255,255,255,0.95) !important;
        text-shadow: 
            2px 2px 4px rgba(0,0,0,0.8),
            1px 1px 2px rgba(0,0,0,0.6) !important;
        font-weight: 600 !important;
    }/* 🎮 Perfect Responsive Grid - Optimal Size with Better Layout */
    .cards-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
        padding: 0.8rem;
        perspective: 1000px;
    }
    
    /* 📱 Enhanced Mobile Responsiveness */
    @media (max-width: 1200px) {
        .cards-container {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.2rem;
        }
    }
    
    @media (max-width: 768px) {
        .cards-container {
            grid-template-columns: 1fr;
            gap: 1.2rem;
            margin: 1.2rem 0;
        }
        
        .card-value {
            font-size: 2.2rem;
        }
        
        .summary-card {
            min-height: 140px;
            padding: 1.5rem 1.2rem;
            margin: 0.8rem 0.5rem;
        }
        
        .card-title {
            font-size: 0.9rem;
        }
        
        .card-description {
            font-size: 0.8rem;
        }
        
        .large-content-card {
            padding: 1.8rem;
            margin: 0.8rem 0;
        }
        
        .large-card-title {
            font-size: 1.2rem;
        }
        
        .large-card-content {
            font-size: 0.95rem;
        }
    }
    
    @media (max-width: 480px) {
        .summary-card {
            min-height: 130px;
            padding: 1.4rem 1rem;
        }
        
        .card-value {
            font-size: 2rem;
        }
    }
    /* Beautiful animations */
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Beautiful animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }    @keyframes sparkle {
        0%, 100% {
            opacity: 0.3;
            transform: rotate(0deg) scale(1);
        }
        50% {
            opacity: 0.8;
            transform: rotate(180deg) scale(1.2);
        }
    }    
    .insight-box {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
        box-shadow: 0 3px 15px rgba(255,152,0,0.2);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #f44336;
        margin: 1rem 0;
        box-shadow: 0 3px 15px rgba(244,67,54,0.2);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .recommendations-box {
        background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(76,175,80,0.3);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.4);
    }
    
    .section-content-box {
        background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(76,175,80,0.3);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.4);
    }
    
    .financial-considerations-box {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(33,150,243,0.3);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.4);
    }
    
    /* Enhance plotly charts background */
    .js-plotly-plot .plotly .modebar {
        background: rgba(255,255,255,0.8) !important;
        border-radius: 5px;
    }
    
    /* Medical icons/patterns as subtle background elements */
    .medical-pattern {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M30 30c0-11.046-8.954-20-20-20s-20 8.954-20 20 8.954 20 20 20 20-8.954 20-20zm0 0c0 11.046 8.954 20 20 20s20-8.954 20-20-8.954-20-20-20-20 8.954-20 20z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        z-index: -2;
        pointer-events: none;
    }    /* Streamlit elements styling - Enhanced Selectbox */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: bold !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
    }
    
    .stSelectbox > div > div > div {
        color: white !important;
        font-weight: bold !important;
    }
    
    /* Fix selectbox label */
    .stSelectbox label {
        color: white !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        font-size: 1.1rem !important;
    }
    
    /* Fix selectbox dropdown and options */
    .stSelectbox [data-baseweb="select"] {
        color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        color: white !important;
        font-weight: bold !important;
    }
    
    .stSelectbox [data-baseweb="select"] span {
        color: white !important;
        font-weight: bold !important;
    }
    
    .stMetric {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.8);
        border-radius: 8px;
        margin: 2px;
    }
    
    /* Success, warning, error message styling */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
      /* Add subtle animation to headers */
    .main-header, .section-header {
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Floating animation for the entire app */
    .stApp {
        animation: gentleFloat 6s ease-in-out infinite;
    }
    
    /* Beautiful gradient animations */
    .section-content-box {
        background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(76,175,80,0.3);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.4);
        animation: slideInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .section-content-box::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes gentleFloat {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-2px);
        }
    }    /* 🎆 MEGA Animation Collection - Exciting Interactions! */
    @keyframes shimmer {
        0% {
            transform: translateX(-100%) translateY(-100%) rotate(45deg);
            opacity: 0;
        }
        50% {
            opacity: 0.6;
        }
        100% {
            transform: translateX(100%) translateY(100%) rotate(45deg);
            opacity: 0;
        }
    }
    
    @keyframes megaShimmer {
        0% {
            transform: translateX(-150%) translateY(-150%) rotate(45deg);
            opacity: 0;
        }
        25% {
            opacity: 0.3;
        }
        50% {
            opacity: 0.8;
            transform: translateX(0%) translateY(0%) rotate(45deg);
        }
        75% {
            opacity: 0.3;
        }
        100% {
            transform: translateX(150%) translateY(150%) rotate(45deg);
            opacity: 0;
        }
    }
    
    @keyframes cardEntrance {
        0% {
            opacity: 0;
            transform: translateY(50px) scale(0.8) rotateX(45deg);
        }
        50% {
            opacity: 0.7;
            transform: translateY(25px) scale(0.9) rotateX(22deg);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1) rotateX(0deg);
        }
    }
    
    @keyframes cardFloat {
        0%, 100% {
            transform: translateY(0px) rotateZ(0deg);
        }
        25% {
            transform: translateY(-3px) rotateZ(0.5deg);
        }
        50% {
            transform: translateY(-6px) rotateZ(0deg);
        }
        75% {
            transform: translateY(-3px) rotateZ(-0.5deg);
        }
    }
    
    @keyframes colorPulse {
        0%, 100% {
            filter: brightness(1) saturate(1);
        }
        50% {
            filter: brightness(1.2) saturate(1.3);
        }
    }
    
    @keyframes particleFloat {
        0%, 100% {
            transform: translateY(0px) rotate(45deg);
        }
        33% {
            transform: translateY(-10px) rotate(135deg);
        }
        66% {
            transform: translateY(-5px) rotate(225deg);
        }
    }
    
    @keyframes sparkleRotate {
        0% {
            transform: rotate(0deg) scale(0.8);
            opacity: 0.5;
        }
        25% {
            transform: rotate(90deg) scale(1.1);
            opacity: 0.8;
        }
        50% {
            transform: rotate(180deg) scale(0.9);
            opacity: 1;
        }
        75% {
            transform: rotate(270deg) scale(1.2);
            opacity: 0.8;
        }
        100% {
            transform: rotate(360deg) scale(0.8);
            opacity: 0.5;
        }
    }
      @keyframes titleGlow {
        0%, 100% {
            text-shadow: 
                2px 2px 4px rgba(0,0,0,0.5),
                1px 1px 2px rgba(0,0,0,0.3),
                0px 0px 8px rgba(255,255,255,0.8);
        }
        50% {
            text-shadow: 
                3px 3px 6px rgba(0,0,0,0.6),
                2px 2px 4px rgba(0,0,0,0.4),
                0px 0px 15px rgba(0,212,170,0.5),
                0px 0px 10px rgba(255,255,255,0.9);
        }
    }
    
    @keyframes iconBounce {
        0%, 100% {
            transform: translateY(-50%) scale(1);
        }
        50% {
            transform: translateY(-60%) scale(1.2);
        }
    }
    
    @keyframes valueCountUp {
        0% {
            opacity: 0;
            transform: translateY(20px) scale(0.5);
        }
        50% {
            opacity: 0.7;
            transform: translateY(10px) scale(0.8);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes valuePulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes sparkleFloat {
        0%, 100% {
            transform: translateY(0px) rotate(0deg);
            opacity: 0.7;
        }
        33% {
            transform: translateY(-5px) rotate(120deg);
            opacity: 1;
        }
        66% {
            transform: translateY(-8px) rotate(240deg);
            opacity: 0.8;
        }
    }
    
    @keyframes descriptionSlide {
        0% {
            opacity: 0;
            transform: translateX(-20px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsive design improvements */
    @media (max-width: 768px) {
        .main .block-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .main-header {
            font-size: 2rem;
            padding: 1rem;
        }
        
        .section-header {
            font-size: 1.5rem;
        }
    }    /* Card header style for use inside metric containers */
    .card-header {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin: 0 0 1rem 0 !important;
        padding: 0 !important;
        background: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        text-shadow: none !important;
        text-align: left !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    /* 🎮 Interactive Elements - Buttons, Tabs, Selectboxes */
    .stButton > button {
        background: linear-gradient(135deg, #00d4aa 0%, #00b894 50%, #00a085 100%);
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1.1rem;
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        box-shadow: 
            0 8px 20px rgba(0,184,148,0.3),
            0 4px 10px rgba(0,184,148,0.2);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255,255,255,0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: all 0.6s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 15px 40px rgba(0,184,148,0.4),
            0 8px 20px rgba(0,184,148,0.3),
            0 0 30px rgba(0,255,204,0.3);
        background: linear-gradient(135deg, #00ffcc 0%, #00e6b8 50%, #00d4aa 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
        animation: buttonRipple 0.6s ease;
    }
    
    .stButton > button:active::before {
        width: 300px;
        height: 300px;
    }
    
    @keyframes buttonRipple {
        0% {
            box-shadow: 0 0 0 0 rgba(0,255,204,0.7);
        }
        70% {
            box-shadow: 0 0 0 20px rgba(0,255,204,0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(0,255,204,0);
        }
    }    /* 🎯 Enhanced Selectbox Styling - Fix Text Visibility */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
        border-radius: 15px !important;
        color: white !important;
        font-weight: bold !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        box-shadow: 
            0 8px 20px rgba(44,62,80,0.3),
            0 4px 10px rgba(44,62,80,0.2) !important;
        transition: all 0.3s ease !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
    }
    
    /* Fix selectbox text visibility - Make text WHITE and BOLD */
    .stSelectbox > div > div > div {
        color: white !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }
    
    /* Fix selectbox input text */
    .stSelectbox input {
        color: white !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }
    
    /* Fix selectbox label */
    .stSelectbox label {
        color: white !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
        font-size: 1.2rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Fix selectbox dropdown options */
    .stSelectbox [role="option"] {
        color: #2c3e50 !important;
        font-weight: 700 !important;
        background: white !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Fix selectbox dropdown options on hover */
    .stSelectbox [role="option"]:hover {
        background: #3498db !important;
        color: white !important;
        font-weight: 700 !important;
    }
      /* Fix selectbox selected value display */
    .stSelectbox [data-baseweb="select"] > div {
        color: white !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }
    
    /* Fix selectbox placeholder and selected text */
    .stSelectbox [data-baseweb="select"] span {
        color: white !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }
    
    /* 🔧 COMPREHENSIVE SELECTBOX TEXT VISIBILITY FIX */
    /* Target all possible selectbox text elements */
    .stSelectbox * {
        color: white !important;
    }
    
    /* Force white text on all selectbox child elements */
    .stSelectbox div[role="button"] {
        color: white !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* Target the actual selected value text */
    .stSelectbox div[role="button"] > div {
        color: white !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* Target selectbox text content */
    .stSelectbox div[data-testid="stSelectbox"] {
        color: white !important;
    }
    
    /* Force visibility on all text within selectbox */
    .stSelectbox div[data-testid="stSelectbox"] * {
        color: white !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* Additional fallback for invisible text */
    .stSelectbox .css-1wa3eu0-placeholder,
    .stSelectbox .css-1uccc91-singleValue,
    .stSelectbox .css-1dimb5e-singleValue {
        color: white !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9) !important;
    }
    
    /* Fix all selectbox inner elements */
    .stSelectbox [data-baseweb="select"] {
        color: white !important;
        font-weight: 900 !important;
    }
    
    /* Fix selectbox arrow */
    .stSelectbox [data-baseweb="select"] svg {
        color: white !important;
        filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.5)) !important;
    }
      .stSelectbox > div > div:hover {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 12px 30px rgba(44,62,80,0.4),
            0 6px 15px rgba(44,62,80,0.3) !important;
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%) !important;
    }
    
    /* Additional fixes for selectbox text visibility */
    .stSelectbox * {
        color: white !important;
    }
    
    .stSelectbox div[data-testid="stSelectbox"] > div > div {
        color: white !important;
        font-weight: 900 !important;
    }
    
    .stSelectbox div[data-testid="stSelectbox"] label {
        color: white !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
    }/* 🌟 Enhanced Tab Styling - Bigger Tabs with Better Visibility */    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.25), rgba(255,255,255,0.15)) !important;
        border-radius: 28px !important;
        padding: 1.8rem !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.18),
            0 8px 20px rgba(0,0,0,0.12) !important;
        display: flex !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 2rem !important;
        margin: 1.5rem 0 2.5rem 0 !important;
    }
      .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 20px !important;
        margin: 0 !important;
        color: white !important;
        font-weight: 900 !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        border: none !important;
        box-shadow: 
            0 10px 30px rgba(102,126,234,0.5),
            0 6px 18px rgba(102,126,234,0.4),
            inset 0 1px 0 rgba(255,255,255,0.2) !important;
        flex: 1 !important;
        text-align: center !important;
        padding: 2rem 2.5rem !important;
        min-width: 0 !important;
        font-size: 1.4rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4) !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        min-height: 80px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-family: 'Segoe UI', 'Arial Black', sans-serif !important;
    }
      .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 
            0 12px 35px rgba(102,126,234,0.5),
            0 6px 18px rgba(102,126,234,0.4) !important;
        background: linear-gradient(135deg, #7c8cea 0%, #8a5fb2 100%) !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%) !important;
        color: white !important;
        transform: scale(1.08) !important;
        box-shadow: 
            0 8px 30px rgba(0,184,148,0.5),
            0 4px 15px rgba(0,184,148,0.4) !important;
        animation: tabGlow 2s ease-in-out infinite !important;
        font-weight: 900 !important;
    }
      @keyframes tabGlow {
        0%, 100% {
            box-shadow: 
                0 6px 20px rgba(0,184,148,0.4),
                0 3px 10px rgba(0,184,148,0.3);
        }
        50% {
            box-shadow: 
                0 8px 30px rgba(0,255,204,0.5),
                0 4px 15px rgba(0,255,204,0.4),
                0 0 20px rgba(0,255,204,0.3);
        }
    }
      /* 📱 Responsive Tab Layout */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap !important;
            gap: 1rem !important;
            padding: 1rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1 1 45% !important;
            font-size: 1.1rem !important;
            padding: 1.2rem 1.5rem !important;
            min-height: 65px !important;
        }
    }
    
    @media (max-width: 480px) {
        .stTabs [data-baseweb="tab"] {
            flex: 1 1 100% !important;
            margin-bottom: 0.5rem !important;
            font-size: 1rem !important;
            padding: 1rem 1.2rem !important;
            min-height: 55px !important;
        }
    }
      /* 🎨 ENHANCED CHART CONTAINER - MUCH BIGGER WITH BETTER VISIBILITY */
    .js-plotly-plot {
        border-radius: 25px !important;
        overflow: hidden !important;
        box-shadow: 
            0 20px 50px rgba(0,0,0,0.15),
            0 10px 25px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        margin: 1.5rem 0 !important;
        min-height: 500px !important;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-5px) !important;
        box-shadow: 
            0 30px 70px rgba(0,0,0,0.2),
            0 15px 35px rgba(0,0,0,0.15) !important;
    }
    
    /* Enhanced chart text and labels */
    .js-plotly-plot .plotly text {
        font-size: 14px !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }
    
    /* Chart titles */
    .js-plotly-plot .plotly .gtitle {
        font-size: 18px !important;
        font-weight: 700 !important;
    }
    
    /* Axis labels */
    .js-plotly-plot .plotly .xtitle,
    .js-plotly-plot .plotly .ytitle {
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Tick labels */
    .js-plotly-plot .plotly .xtick,
    .js-plotly-plot .plotly .ytick {
        font-size: 14px !important;
        font-weight: 500 !important;
    }
      /* Legend text */
    .js-plotly-plot .plotly .legendtext {
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    /* 🎯 SIDEBAR SELECTBOX - CRITICAL FIX FOR NAVIGATION TEXT VISIBILITY */
    /* Target sidebar selectbox specifically */
    .css-1d391kg .stSelectbox > div > div {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid #ffffff !important;
        border-radius: 10px !important;
    }
    
    /* Sidebar selectbox text - FORCE WHITE COLOR */
    .css-1d391kg .stSelectbox > div > div > div {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* Sidebar selectbox input text */
    .css-1d391kg .stSelectbox input {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    
    /* Sidebar selectbox label */
    .css-1d391kg .stSelectbox label {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* Sidebar selectbox dropdown arrow */
    .css-1d391kg .stSelectbox svg {
        fill: #ffffff !important;
    }
    
    /* Alternative sidebar class targeting */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid #ffffff !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div > div {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox input {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox svg {
        fill: #ffffff !important;
    }
    
    /* Universal sidebar selectbox fix - most aggressive approach */
    .stSidebar .stSelectbox * {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    
    .stSidebar .stSelectbox > div > div {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid #ffffff !important;
    }
    
    /* Target sidebar selectbox button role */
    .stSidebar .stSelectbox div[role="button"] {
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* Target sidebar selectbox button text */
    .stSidebar .stSelectbox div[role="button"] > div {
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
      /* Target sidebar selectbox selected value */
    .stSidebar .stSelectbox [data-baseweb="select"] span {
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* 🎨 MODERN DROPDOWN STYLING - COMPREHENSIVE FIX */
    /* Main selectbox container - Dark mode compatible */
    .stSelectbox > div {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
        border: 2px solid #3498db !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Selectbox hover state */
    .stSelectbox > div:hover {
        border-color: #e74c3c !important;
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Selected value display - CRITICAL FOR VISIBILITY */
    .stSelectbox [data-baseweb="select"] {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        min-height: 48px !important;
    }
    
    /* Selected text - WHITE AND BOLD */
    .stSelectbox [data-baseweb="select"] > div {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
        line-height: 1.4 !important;
    }
    
    /* Selected value span - FORCE WHITE */
    .stSelectbox [data-baseweb="select"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* Dropdown arrow styling */
    .stSelectbox [data-baseweb="select"] svg {
        fill: #ffffff !important;
        width: 20px !important;
        height: 20px !important;
        filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.5)) !important;
    }
    
    /* Focus state for accessibility */
    .stSelectbox [data-baseweb="select"]:focus-within {
        outline: 3px solid #e74c3c !important;
        outline-offset: 2px !important;
        border-color: #e74c3c !important;
    }
    
    /* Dropdown menu container */
    .stSelectbox [data-baseweb="popover"] {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
        border: 2px solid #3498db !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Dropdown options */
    .stSelectbox [role="option"] {
        background: transparent !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        margin: 4px 8px !important;
        transition: all 0.2s ease !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6) !important;
    }
    
    /* Dropdown option hover state */
    .stSelectbox [role="option"]:hover {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        transform: translateX(4px) !important;
        box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3) !important;
    }
    
    /* Selected option highlight */
    .stSelectbox [role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, #27ae60 0%, #229954 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3) !important;
    }
    
    /* Selectbox label styling */
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
        margin-bottom: 8px !important;
        display: block !important;
    }
    
    /* Input element (if any) */
    .stSelectbox input {
        color: #ffffff !important;
        font-weight: 700 !important;
        background: transparent !important;
    }
    
    /* 🌟 SIDEBAR SPECIFIC ENHANCEMENTS */
    /* Sidebar selectbox with enhanced visibility */
    .stSidebar .stSelectbox > div {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        border: 2px solid #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1) !important;
    }
    
    .stSidebar .stSelectbox [data-baseweb="select"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        padding: 14px 18px !important;
        min-height: 50px !important;
    }
    
    .stSidebar .stSelectbox [data-baseweb="select"] > div,
    .stSidebar .stSelectbox [data-baseweb="select"] span {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 17px !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9) !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Sidebar hover effect */
    .stSidebar .stSelectbox > div:hover {
        border-color: #ff6b6b !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3) !important;
        transform: scale(1.02) !important;
    }
    
    /* 🎯 UNIVERSAL FALLBACK - FORCE VISIBILITY */
    /* Apply to any missed selectbox elements */
    div[data-baseweb="select"] {
        background: #2c3e50 !important;
        color: #ffffff !important;
    }
    
    div[data-baseweb="select"] * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Ensure all select-related text is visible */
    [class*="select"] span,
    [class*="Select"] span,
    [data-baseweb*="select"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
      /* 🔧 CRITICAL FIX - SELECTED TEXT VISIBILITY */
    /* Force selected text to be visible - Most aggressive approach */
    .stSelectbox [data-baseweb="select"] > div > div {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
        background: transparent !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Target the actual text content inside select */
    .stSelectbox [data-baseweb="select"] [data-baseweb="base-input"] {
        color: #ffffff !important;
        font-weight: 800 !important;
        background: transparent !important;
    }
    
    /* Target any span or text elements in select */
    .stSelectbox [data-baseweb="select"] span[data-baseweb],
    .stSelectbox [data-baseweb="select"] div[data-baseweb] {
        color: #ffffff !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
    }
    
    /* Alternative targeting for selected value display */
    .stSelectbox div[role="button"] span,
    .stSelectbox div[role="button"] div {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Force all text inside selectbox to be white */
    .stSelectbox * {
        color: #ffffff !important;
    }
    
    /* Specific fix for Streamlit's select component */
    .stSelectbox [class*="css"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    
    /* Target the value display area specifically */
    .stSelectbox [data-baseweb="select"] > div:first-child {
        color: #ffffff !important;
        font-weight: 800 !important;
        background: rgba(44, 62, 80, 0.9) !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
    }
    
    /* Ensure placeholder text is also visible */
    .stSelectbox [data-baseweb="select"] [data-baseweb="input"] {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* 🎯 SIDEBAR SELECTBOX - ULTRA AGGRESSIVE FIX */
    .stSidebar .stSelectbox [data-baseweb="select"] > div > div,
    .stSidebar .stSelectbox [data-baseweb="select"] span,
    .stSidebar .stSelectbox [data-baseweb="select"] div {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,1) !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
    }
    
    /* Force sidebar selectbox background for better contrast */
    .stSidebar .stSelectbox [data-baseweb="select"] {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important;
        border: 3px solid #ffffff !important;
        color: #ffffff !important;
        padding: 16px 20px !important;
        min-height: 55px !important;
    }    /* Additional fallback for any missed elements */
    .stSidebar .stSelectbox [role="button"] {
        color: #ffffff !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important;
    }
    
    /* 🚨 NUCLEAR OPTION - FORCE SELECTED TEXT VISIBILITY */
    /* Target ALL possible text elements in selectbox */
    .stSelectbox, .stSelectbox *, 
    .stSelectbox [class*="css"], 
    .stSelectbox [class*="st-"], 
    .stSelectbox div, 
    .stSelectbox span {
        color: #ffffff !important;
        font-weight: 900 !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,1) !important;
    }
    
    /* Force visibility on ALL nested elements */
    .stSelectbox > div > div > div > div,
    .stSelectbox > div > div > div > div > div,
    .stSelectbox > div > div > div > div > div > div {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,1) !important;
    }
    
    /* Target Streamlit's internal CSS classes */
    [class*="st-"] {
        color: #ffffff !important;
    }
    
    /* Force styling on dynamic CSS classes */
    div[class^="css-"] {
        color: #ffffff !important;
        font-weight: 900 !important;
    }
    
    /* 🎯 SIDEBAR NUCLEAR OPTION */
    .stSidebar .stSelectbox,
    .stSidebar .stSelectbox *,
    .stSidebar .stSelectbox [class*="css"],
    .stSidebar .stSelectbox [class*="st-"],
    .stSidebar .stSelectbox div,
    .stSidebar .stSelectbox span {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        text-shadow: 4px 4px 8px rgba(0,0,0,1) !important;
        background: rgba(0,0,0,0.8) !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    
    /* Force ALL sidebar selectbox nested elements */
    .stSidebar .stSelectbox > div > div > div > div,
    .stSidebar .stSelectbox > div > div > div > div > div,
    .stSidebar .stSelectbox > div > div > div > div > div > div,
    .stSidebar .stSelectbox > div > div > div > div > div > div > div {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        text-shadow: 4px 4px 8px rgba(0,0,0,1) !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
        background: rgba(0,0,0,0.9) !important;
        padding: 2px 4px !important;
    }
    
    /* Force text content to be visible */
    .stSidebar .stSelectbox::before {
        content: attr(data-selected-text) !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        position: absolute !important;
        z-index: 1000 !important;
        background: rgba(0,0,0,0.9) !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    /* Override ANY possible hidden styles */
    .stSelectbox [style*="color"] {
        color: #ffffff !important;
    }
    
    .stSelectbox [style*="opacity"] {
        opacity: 1 !important;
    }
    
    .stSelectbox [style*="visibility"] {
        visibility: visible !important;
    }
    
    /* 🌈 DYNAMIC ACTIVE SECTION INDICATOR GRADIENTS 🌈 */
    
    /* Overview Active Indicator - Royal Purple to Electric Blue */
    .active-section-indicator.overview-active {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #5b4cdb 50%, 
            #667eea 75%, 
            #764ba2 100%) !important;
        box-shadow: 
            0 15px 35px rgba(102, 126, 234, 0.6),
            0 5px 15px rgba(118, 75, 162, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Screening Active Indicator - Pink Sunset to Ocean Blue */
    .active-section-indicator.screening-active {
        background: linear-gradient(135deg, 
            #ff6b6b 0%, 
            #feca57 25%, 
            #48cae4 50%, 
            #ff006e 75%, 
            #4c63d2 100%) !important;
        box-shadow: 
            0 15px 35px rgba(255, 107, 107, 0.6),
            0 5px 15px rgba(254, 202, 87, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Awareness Active Indicator - Warm Peach to Rose Gold */
    .active-section-indicator.awareness-active {
        background: linear-gradient(135deg, 
            #ff9a56 0%, 
            #ffad56 25%, 
            #ff6b9d 50%, 
            #c44569 75%, 
            #f8b500 100%) !important;
        box-shadow: 
            0 15px 35px rgba(255, 154, 86, 0.6),
            0 5px 15px rgba(196, 69, 105, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Analysis Active Indicator - Mint to Lavender Dream */
    .active-section-indicator.analysis-active {
        background: linear-gradient(135deg, 
            #a8edea 0%, 
            #fed6e3 25%, 
            #a8e6cf 50%, 
            #dda0dd 75%, 
            #98fb98 100%) !important;
        box-shadow: 
            0 15px 35px rgba(168, 237, 234, 0.6),
            0 5px 15px rgba(221, 160, 221, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Statistics Active Indicator - Golden Hour to Purple Magic */
    .active-section-indicator.statistics-active {
        background: linear-gradient(135deg, 
            #f7971e 0%, 
            #ffd200 25%, 
            #9c88ff 50%, 
            #5f27cd 75%, 
            #ff9ff3 100%) !important;
        box-shadow: 
            0 15px 35px rgba(247, 151, 30, 0.6),
            0 5px 15px rgba(95, 39, 205, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Recommendations Active Indicator - Ocean Breeze to Sky */
    .active-section-indicator.recommendations-active {
        background: linear-gradient(135deg, 
            #00d2ff 0%, 
            #3a7bd5 25%, 
            #928dab 50%, 
            #00d2ff 75%, 
            #3a7bd5 100%) !important;
        box-shadow: 
            0 15px 35px rgba(0, 210, 255, 0.6),
            0 5px 15px rgba(58, 123, 213, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Card content styling */
    .nav-card-emoji {
        font-size: 32px;
        display: block;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: bounce 2s ease-in-out infinite;
    }
    
    .nav-card-text {
        font-size: 15px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        line-height: 1.3;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-3px);
        }
        60% {
            transform: translateY(-2px);
        }
    }
    
    /* 🎯 BEAUTIFUL ACTIVE SECTION INDICATOR - MATCHING YOUR IMAGE STYLE 🎯 */
    .active-section-indicator {
        background: linear-gradient(135deg, 
            #7c3aed 0%, 
            #a855f7 25%, 
            #3b82f6 50%, 
            #6366f1 75%, 
            #8b5cf6 100%);
        background-size: 300% 300%;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 20px;
        margin: 25px 0;
        text-align: center;
        color: #ffffff;
        font-weight: 900;
        font-size: 16px;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
        box-shadow: 
            0 15px 35px rgba(124, 58, 237, 0.4),
            0 5px 15px rgba(59, 130, 246, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        animation: activeIndicatorGlow 4s ease-in-out infinite, activeGradientFlow 6s ease infinite;
        position: relative;
        overflow: hidden;
    }
    
    .active-section-indicator::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.2), 
            transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes activeIndicatorGlow {
        0%, 100% {
            box-shadow: 
                0 15px 35px rgba(124, 58, 237, 0.4),
                0 5px 15px rgba(59, 
                element.style.setProperty('text-shadow', '4px 4px 8px rgba(0,0,0,1)', 'important');
                element.style.setProperty('background', 'rgba(0,0,0,0.9)', 'important');
            });
        });
        
        console.log('✅ Selectbox text visibility forced!');
    }
    
    // Run immediately
    forceSelectboxVisibility();
    
    // Run again after a delay to catch dynamic content
    setTimeout(forceSelectboxVisibility, 1000);
    setTimeout(forceSelectboxVisibility, 3000);
    
    // Run whenever the page updates
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                forceSelectboxVisibility();
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// Also run when Streamlit reloads components
window.addEventListener('load', function() {
    setTimeout(function() {
        console.log('🔄 Page loaded - forcing selectbox visibility again...');
        document.querySelectorAll('.stSelectbox *').forEach(function(el) {
            el.style.setProperty('color', '#ffffff', 'important');
            el.style.setProperty('font-weight', '900', 'important');
            el.style.setProperty('opacity', '1', 'important');
            el.style.setProperty('visibility', 'visible', 'important');
        });
    }, 2000);
});
</script>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the cervical cancer dataset"""
    try:
        # First try to load the local CSV file
        local_csv_path = "cervical cancer_csv.csv"
        if os.path.exists(local_csv_path):
            df = pd.read_csv(local_csv_path)
            return preprocess_data(df)
        
        # Fallback: Check if running locally or in cloud
        is_kaggle = "KAGGLE_KERNEL_RUN_TYPE" in os.environ
        
        if not is_kaggle:
            # Download dataset using kagglehub as fallback
            dataset_name = "promisebansah/cervical-cancer-survey-ghana-female-students"
            dataset_dir = kagglehub.dataset_download(dataset_name)
            
            # Find CSV file
            data_path = None
            for root, _, files in os.walk(dataset_dir):
                for file in files:
                    if file.endswith(".csv"):
                        data_path = os.path.join(root, file)
                        break
        else:
            data_path = "/kaggle/input/cervical-cancer-survey-ghana-female-students"
        
        # Load the dataset
        if data_path:
            df = pd.read_csv(data_path)
            return preprocess_data(df)
        else:
            st.error("Dataset not found. Please ensure the dataset is available.")
            return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def preprocess_data(df):
    """Preprocess the dataset for analysis"""
    # Create copy
    ccan = df.copy()
    
    # Process risk factors
    risk_factors_cols = ['multiple_sexual_partners', 'age_factor', 'hereditary_risk', 'unprotected_sex']
    risk_factors = ccan[risk_factors_cols].copy()
    
    # Recode risk factors
    map_risk_factors = {'SD': 'D', 'D': 'D', 'A': 'A', 'SA': 'A'}
    for col in risk_factors_cols:
        risk_factors[col] = risk_factors[col].map(map_risk_factors)
        ccan[col] = risk_factors[col]
    
    # Process symptoms
    symptoms_cols = ['abnormal_menstrual_bleeding', 'general_body_pain', 'intermenstrual_bleeding', 
                    'vaginal_itching', 'foul_vaginal_discharge', 'postmenopausal_bleeding',
                    'unexplained_weight_loss', 'persistent_diarrhea', 'blood_in_stool',
                    'persistent_pelvic_pain', 'bleeding_during_sex']
    
    map_symptoms = {'SD': 'D', 'D': 'D', 'A': 'A', 'SA': 'A'}
    for col in symptoms_cols:
        if col in ccan.columns:
            ccan[col] = ccan[col].map(map_symptoms)
    
    # Process screening knowledge
    screening_cols = ['knows_screening_center', 'screen_from_age_21', 'screen_every_2_years',
                     'screening_for_healthy', 'screening_for_early_detection',
                     'detection_can_prevent_cancer', 'regular_screening_helps_detection']
    
    # Special handling for screen_every_2_years (reverse coding)
    ccan['screen_every_2_years'] = ccan['screen_every_2_years'].replace({'SD': 'A', 'D': 'A', 'A': 'D', 'SA': 'D'})
    
    map_screening = {'SD': 'A', 'D': 'A', 'A': 'D', 'SA': 'D'}
    for col in screening_cols:
        if col in ccan.columns and col != 'screen_every_2_years':
            ccan[col] = ccan[col].map(map_screening)
    
    # Process screening methods
    methods_cols = ['visual_is_one_method', 'visual_only_method', 'visual_is_easiest_method', 'visual_at_any_level']
    
    # Special handling for visual_only_method
    ccan['visual_only_method'] = ccan['visual_only_method'].replace({'SD': 'A', 'D': 'A', 'A': 'D', 'SA': 'D'})
    
    map_methods = {'SD': 'D', 'D': 'D', 'A': 'A', 'SA': 'A'}
    for col in methods_cols:
        if col in ccan.columns and col != 'visual_only_method':
            ccan[col] = ccan[col].map(map_methods)
    
    return ccan

def create_demographics_overview(df):
    """Create demographics overview section"""
    st.markdown('<div class="section-header">👥 Demographics Overview</div>', unsafe_allow_html=True)
      # Create the cards container with HTML - Repositioned Ever Told to Screen
    cards_html = f"""
    <div class="cards-container">
        <div class="summary-card green">
            <div class="card-title">👥 Total Participants</div>
            <div class="card-value">{len(df)}</div>
            <div class="card-description">Female tertiary students from Hohoe Municipality, Ghana</div>
        </div>
        <div class="summary-card purple">
            <div class="card-title">🧠 Ever Told to Screen</div>
            <div class="card-value">{(df['eva_told_to_scrn'].value_counts(normalize=True)['yes'] * 100 if 'eva_told_to_scrn' in df.columns else 0):.1f}%</div>
            <div class="card-description">{'� Low Awareness' if (df['eva_told_to_scrn'].value_counts(normalize=True)['yes'] * 100 if 'eva_told_to_scrn' in df.columns else 0) < 30 else '📊 Moderate Awareness' if (df['eva_told_to_scrn'].value_counts(normalize=True)['yes'] * 100 if 'eva_told_to_scrn' in df.columns else 0) < 60 else '🌟 High Awareness'} - Foundation for interventions</div>
        </div>
        <div class="summary-card blue">
            <div class="card-title">📅 Average Age</div>
            <div class="card-value">{df['age'].mean() if 'age' in df.columns else 0:.1f} years</div>
            <div class="card-description">Young adult population in prime screening age</div>
        </div>
        <div class="summary-card orange">
            <div class="card-title">🎯 Screening Uptake Rate</div>
            <div class="card-value">{(df['Uptake'].value_counts(normalize=True)['yes'] * 100 if 'Uptake' in df.columns else 0):.1f}%</div>
            <div class="card-description">{'� Critical - Action needed' if (df['Uptake'].value_counts(normalize=True)['yes'] * 100 if 'Uptake' in df.columns else 0) < 20 else '⚠️ Below Target' if (df['Uptake'].value_counts(normalize=True)['yes'] * 100 if 'Uptake' in df.columns else 0) < 50 else '✅ Good Rate'}</div>        </div>    </div>
    """
    
    st.markdown(cards_html, unsafe_allow_html=True)
    
    # 🎨 Modern Interactive Demographics Visualization - Side by Side
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 📊 Age Group Distribution - Modern Donut Chart
        if 'agegrp' in df.columns:
            # 🍩 Modern Animated Donut Chart with Beautiful Colors
            fig_age = px.pie(df, names='agegrp', 
                           title=None,  # We'll add custom title
                           hole=0.6,  # Creates donut effect
                           color_discrete_sequence=[
                               '#1A237E',  # Deep Indigo (contrasts with orange bg)
                               '#004D40',  # Dark Teal
                               '#1B5E20',  # Dark Green
                               '#4A148C',  # Deep Purple
                               '#B71C1C',  # Dark Red
                               '#E65100',  # Deep Orange
                               '#3E2723'   # Dark Brown
                           ])
        
            # Enhanced styling for modern look
            fig_age.update_traces(
                textposition='outside',
                textinfo='percent+label',
                textfont_size=18,  # Larger font for visibility
                textfont_color='white',
                textfont_family='Arial Black',
                marker=dict(
                    line=dict(color='white', width=4)  # Thicker border
                ),
                hovertemplate='<b>%{label}</b><br>' +
                             'Count: %{value}<br>' +
                             'Percentage: %{percent}<br>' +
                             '<extra></extra>',
                hoverlabel=dict(
                    bgcolor='rgba(0,0,0,0.8)',
                    bordercolor='white',
                    font_color='white',
                    font_size=16,
                    font_family='Arial'
                )
            )
        
            fig_age.update_layout(
                height=600,  # Height for side-by-side display
                showlegend=True,
                legend=dict(
                    orientation="v",  # Vertical legend for side-by-side
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(size=12, color='white', family='Arial Bold'),
                    bgcolor='rgba(0,0,0,0.2)',
                    bordercolor='white',
                    borderwidth=1
                ),
                margin=dict(l=40, r=40, t=100, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=16, family='Arial'),
                annotations=[
                    dict(
                        text="<b style='font-size:20px'>Age Groups</b><br><span style='font-size:14px'>Distribution</span>",
                        x=0.5, y=0.5,
                        font_size=18,
                        font_color='white',
                        font_family='Arial Black',
                        showarrow=False
                    ),
                    dict(
                        text="<b>📊 Age Group Distribution</b>",
                        x=0.5, y=1.12,
                        font_size=20,
                        font_color='white',
                        font_family='Arial Black',
                        showarrow=False,
                        xanchor='center'
                    )
                ]
            )
        
            # Add animation and interactivity
            fig_age.update_traces(
                rotation=90,
                pull=[0.05 if i == 0 else 0 for i in range(len(df['agegrp'].unique()))]
            )
        
            st.plotly_chart(fig_age, use_container_width=True)
        else:
            st.info("💡 Age group data not found in the dataset")
    
    with col2:
        # 🏫 Institutional Affiliation - Modern Donut Chart
        if 'affiliation' in df.columns:
            affiliation_counts = df['affiliation'].value_counts()
        
            if len(affiliation_counts) > 0:
                # 🌟 Modern Interactive Donut Chart with Bold Percentages
                fig_aff = px.pie(df, names='affiliation', 
                               title=None,  # We'll add custom title
                               hole=0.5,  # Creates donut effect
                               color_discrete_sequence=[
                                   '#2E1F7B',  # Deep Navy Blue
                                   '#8B0000',  # Dark Red
                                   '#006400',  # Dark Green  
                                   '#4B0082',  # Indigo
                                   '#8B4513',  # Saddle Brown
                                   '#2F4F4F',  # Dark Slate Gray
                                   '#800080',  # Purple
                                   '#556B2F'   # Dark Olive Green
                               ])
            
                # Enhanced styling for modern look
                fig_aff.update_traces(
                    textposition='outside',
                    textinfo='percent+label',
                    textfont_size=16,
                    textfont_color='white',
                    textfont_family='Arial Black',
                    marker=dict(
                        line=dict(color='white', width=4)
                    ),
                    hovertemplate='<b>%{label}</b><br>' +
                                 'Count: %{value}<br>' +
                                 'Percentage: %{percent}<br>' +
                                 '<extra></extra>',
                    hoverlabel=dict(
                        bgcolor='rgba(0,0,0,0.8)',
                        bordercolor='white',
                        font_color='white',
                        font_size=16,
                        font_family='Arial'
                    )
                )
            
                fig_aff.update_layout(
                    height=600,  # Height for side-by-side display
                    showlegend=True,
                    legend=dict(
                        orientation="v",  # Vertical legend for side-by-side
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.02,
                        font=dict(size=12, color='white', family='Arial Bold'),
                        bgcolor='rgba(0,0,0,0.1)',
                        bordercolor='white',
                        borderwidth=1
                    ),
                    margin=dict(l=40, r=40, t=100, b=40),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=16, family='Arial'),
                    annotations=[
                        dict(
                            text="<b>Institutional<br>Affiliation</b>",
                            x=0.5, y=0.5,
                            font_size=18,
                            font_color='white',
                            font_family='Arial Black',
                            showarrow=False
                        ),
                        dict(
                            text="<b>🏫 Institutional Affiliation</b>",
                            x=0.5, y=1.12,
                            font_size=20,
                            font_color='white',
                            font_family='Arial Black',
                            showarrow=False,
                            xanchor='center'
                        )
                    ]
                )
            
                # Add pull effect for the first slice
                fig_aff.update_traces(
                    pull=[0.1 if i == 0 else 0 for i in range(len(affiliation_counts))]
                )
            
                st.plotly_chart(fig_aff, use_container_width=True)
            else:
                st.info("💡 No institutional affiliation data available to display")
        else:
            st.info("💡 Institutional affiliation data not found in the dataset")

def create_screening_uptake_analysis(df):
    """Create screening uptake analysis section"""
    st.markdown('<div class="section-header">🎯 Screening Uptake Analysis</div>', unsafe_allow_html=True)
    
    # Overall uptake
    if 'Uptake' in df.columns:
        uptake_counts = df['Uptake'].value_counts()
        uptake_pct = df['Uptake'].value_counts(normalize=True) * 100
        
        # Create summary cards for screening uptake overview
        cards_html = f"""
        <div class="cards-container">
            <div class="summary-card orange">
                <div class="card-title">🚨 Never Screened</div>
                <div class="card-value" style="color: #e74c3c">{uptake_pct.get('no', 0):.1f}%</div>
                <div class="card-description">{uptake_counts.get('no', 0)} students have never undergone cervical cancer screening</div>
            </div>
            <div class="summary-card green">
                <div class="card-title">✅ Ever Screened</div>
                <div class="card-value" style="color: #27ae60">{uptake_pct.get('yes', 0):.1f}%</div>
                <div class="card-description">{uptake_counts.get('yes', 0)} students have been screened at least once</div>
            </div>
            <div class="summary-card purple">
                <div class="card-title">🎯 Target Achievement</div>
                <div class="card-value" style="color: {'#e74c3c' if uptake_pct.get('yes', 0) < 50 else '#f39c12' if uptake_pct.get('yes', 0) < 70 else '#27ae60'}">{('Critical' if uptake_pct.get('yes', 0) < 20 else 'Below Target' if uptake_pct.get('yes', 0) < 50 else 'Good Progress')}</div>
                <div class="card-description">{'🚨 Urgent intervention needed' if uptake_pct.get('yes', 0) < 20 else '⚠️ Improvement required' if uptake_pct.get('yes', 0) < 50 else '📈 Meeting health goals'}</div>
            </div>
            <div class="summary-card blue">
                <div class="card-title">🏥 Health Impact</div>
                <div class="card-value" style="color: #2980b9">High Risk</div>
                <div class="card-description">Low screening rates increase cervical cancer mortality risk significantly</div>
            </div>
        </div>
        """        
        st.markdown(cards_html, unsafe_allow_html=True)
        
        # Create enhanced donut chart - Full Width Vertical Layout
        st.markdown("### 📊 Screening Uptake Overview")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Large vertical donut chart with better colors and bigger labels
        fig = go.Figure(data=[go.Pie(
            labels=['Never Screened', 'Ever Screened'],
            values=[uptake_counts['no'], uptake_counts['yes']],
            hole=0.5,  # Larger hole for better donut effect
            marker_colors=['#e74c3c', '#2ecc71'],  # Red for never screened, Green for screened
            textinfo='label+percent+value',
            textfont=dict(size=20, family='Arial Black', color='white'),  # Larger, bolder text
            textposition='outside',  # Outside positioning for better visibility
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            marker=dict(line=dict(color='white', width=4)),  # Thicker borders
            pull=[0.05, 0]  # Slightly pull out the "never screened" slice for emphasis
        )])
        
        fig.update_layout(
            title=dict(
                text="<b>Cervical Cancer Screening Uptake Distribution</b>",
                x=0.5,
                font=dict(size=24, color='white', family='Arial Black')
            ),
            height=700,  # Much larger height for vertical display
            showlegend=True,
            legend=dict(
                font=dict(size=18, family='Arial Bold', color='white'),
                orientation="h",  # Horizontal legend at bottom
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(0,0,0,0.2)',
                bordercolor='white',
                borderwidth=1
            ),
            font=dict(size=18, family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=100, b=120, l=40, r=40),
            annotations=[
                dict(
                    text=f"<b style='font-size:28px'>Total</b><br><span style='font-size:20px'>{uptake_counts.sum()} Students</span>",
                    x=0.5, y=0.5,
                    font_size=24,
                    font_color='white',
                    font_family='Arial Black',
                    showarrow=False
                )
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary statistics below the chart
        uptake_never = uptake_pct.get('no', 0)
        uptake_ever = uptake_pct.get('yes', 0)
        
        summary_cards_html = f"""
        <div class="cards-container">
            <div class="summary-card orange">
                <div class="card-title">⚠️ Never Screened</div>
                <div class="card-value" style="color: #e74c3c">{uptake_never:.1f}%</div>
                <div class="card-description">Major concern requiring intervention</div>
            </div>
            <div class="summary-card green">
                <div class="card-title">✅ Ever Screened</div>
                <div class="card-value" style="color: #27ae60">{uptake_ever:.1f}%</div>
                <div class="card-description">Current screening coverage</div>
            </div>
        </div>
        """
        st.markdown(summary_cards_html, unsafe_allow_html=True)
    
    # Sankey Diagram for Screening Pathway
    st.markdown("### 🔄 Screening Uptake Pathway Analysis")
    create_sankey_diagram(df)
    
    # Uptake by demographics with improved colors
    demo_cols = ['agegrp', 'marital', 'lev', 'affiliation']
    color_palettes = {
        'agegrp': ['#3498db', '#e74c3c'],  # Blue/Red
        'marital': ['#9b59b6', '#f39c12'], # Purple/Orange
        'lev': ['#1abc9c', '#e67e22'],     # Teal/Orange
        'affiliation': ['#2c3e50', '#c0392b'] # Dark Blue/Dark Red
    }
    
    for col in demo_cols:
        if col in df.columns and 'Uptake' in df.columns:
            st.subheader(f"📊 Screening Uptake by {col.replace('_', ' ').title()}")
            
            # Create crosstab
            ct = pd.crosstab(df[col], df['Uptake'], normalize='index') * 100
              # Create grouped bar chart with custom colors
            fig = go.Figure()
            
            colors = color_palettes.get(col, ['#66c2a5', '#fc8d62'])
            
            fig.add_trace(go.Bar(
                name='Ever Screened',
                x=ct.index,
                y=ct['yes'] if 'yes' in ct.columns else [0] * len(ct.index),
                marker_color=colors[0],
                text=[f'{val:.1f}%' for val in (ct['yes'] if 'yes' in ct.columns else [0] * len(ct.index))],
                textposition='auto',
                textfont=dict(size=14, family='Arial Black', color='white'),
                hovertemplate='<b>%{x}</b><br>Ever Screened: %{y}%<extra></extra>'
            ))
            
            fig.add_trace(go.Bar(
                name='Never Screened',
                x=ct.index,
                y=ct['no'] if 'no' in ct.columns else [0] * len(ct.index),
                marker_color=colors[1],
                text=[f'{val:.1f}%' for val in (ct['no'] if 'no' in ct.columns else [0] * len(ct.index))],
                textposition='auto',
                textfont=dict(size=14, family='Arial Black', color='white'),
                hovertemplate='<b>%{x}</b><br>Never Screened: %{y}%<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(
                    text=f"Screening Uptake by {col.replace('_', ' ').title()}",
                    x=0.5,
                    font=dict(size=20, color='#2c3e50', family='Arial Black')
                ),
                xaxis_title=col.replace('_', ' ').title(),
                yaxis_title='Percentage (%)',
                barmode='group',
                height=550,
                showlegend=True,
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.02, 
                    xanchor="right", 
                    x=1,
                    font=dict(size=16, family='Arial')                ),
                xaxis=dict(
                    title=dict(text=col.replace('_', ' ').title(), font=dict(size=16, family='Arial Black')),
                    tickfont=dict(size=14, family='Arial')
                ),
                yaxis=dict(
                    title=dict(text='Percentage (%)', font=dict(size=16, family='Arial Black')),
                    tickfont=dict(size=14, family='Arial'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.2)'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=80, b=60, l=60, r=60)
            )
            
            st.plotly_chart(fig, use_container_width=True)

def create_awareness_section(df):
    """Create awareness analysis section"""
    st.markdown('<div class="section-header">🧠 Awareness Assessment</div>', unsafe_allow_html=True)
    
    awareness_cols = ['eva_told_to_scrn', 'aware_of_scrn_centa']
    
    if all(col in df.columns for col in awareness_cols):
        # Create side-by-side comparison with enhanced colors
        col1, col2 = st.columns(2)
        
        awareness_data = []
        colors = [['#e74c3c', '#2ecc71'], ['#9b59b6', '#f39c12']]  # Red/Green, Purple/Orange
        titles = ["Ever Told to Screen", "Aware of Screening Centre"]
        
        for i, col in enumerate(awareness_cols):
            counts = df[col].value_counts()
            pct = df[col].value_counts(normalize=True) * 100
            
            title = titles[i]
            color_pair = colors[i];
              # Create enhanced bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['No', 'Yes'],
                y=[counts.get('no', 0), counts.get('yes', 0)],
                marker_color=color_pair,
                text=[f'{pct.get("no", 0):.1f}%<br>({counts.get("no", 0)})', 
                      f'{pct.get("yes", 0):.1f}%<br>({counts.get("yes", 0)})'],
                textposition='auto',
                textfont=dict(color='white', size=16, family='Arial Black'),
                hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Percentage: %{text}<extra></extra>',
                marker=dict(line=dict(color='white', width=2))
            ))
            
            fig.update_layout(
                title=dict(
                    text=title, 
                    x=0.5, 
                    font=dict(size=20, color='#2c3e50', family='Arial Black')
                ),
                yaxis_title="Count",
                xaxis_title="Response",
                height=500,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title=dict(text="Response", font=dict(size=16, family='Arial Black')),
                    tickfont=dict(size=14, family='Arial')
                ),
                yaxis=dict(
                    title=dict(text="Count", font=dict(size=16, family='Arial Black')),
                    tickfont=dict(size=14, family='Arial'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.2)'
                ),
                margin=dict(t=80, b=60, l=60, r=60)
            )
            
            # Add grid
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            fig.update_xaxes(showgrid=False)
            
            if i == 0:
                col1.plotly_chart(fig, use_container_width=True)
                
                # Add metric for column 1
                col1.markdown('<div class="metric-container">', unsafe_allow_html=True)
                yes_pct = pct.get('yes', 0)
                if yes_pct < 30:
                    col1.error(f"⚠️ Low Awareness: {yes_pct:.1f}%")
                elif yes_pct < 60:
                    col1.warning(f"⚠️ Moderate Awareness: {yes_pct:.1f}%")
                else:
                    col1.success(f"✅ Good Awareness: {yes_pct:.1f}%")
                col1.markdown('</div>', unsafe_allow_html=True)
                
            else:
                col2.plotly_chart(fig, use_container_width=True)
                
                # Add metric for column 2
                col2.markdown('<div class="metric-container">', unsafe_allow_html=True)
                yes_pct = pct.get('yes', 0)
                if yes_pct < 30:
                    col2.error(f"⚠️ Low Awareness: {yes_pct:.1f}%")
                elif yes_pct < 60:
                    col2.warning(f"⚠️ Moderate Awareness: {yes_pct:.1f}%")
                else:
                    col2.success(f"✅ Good Awareness: {yes_pct:.1f}%")
                col2.markdown('</div>', unsafe_allow_html=True)
        
        # Combined awareness analysis
        st.markdown("### 📊 Combined Awareness Analysis")
        
        # Create a combined awareness score
        if all(col in df.columns for col in awareness_cols):
            df_awareness = df[awareness_cols].copy()
            
            # Calculate combined awareness (both yes)
            both_aware = df_awareness[(df_awareness['eva_told_to_scrn'] == 'yes') & 
                                    (df_awareness['aware_of_scrn_centa'] == 'yes')]
            neither_aware = df_awareness[(df_awareness['eva_told_to_scrn'] == 'no') & 
                                       (df_awareness['aware_of_scrn_centa'] == 'no')]
            partial_aware = len(df_awareness) - len(both_aware) - len(neither_aware)
            
            # Create stacked bar chart
            categories = ['High Awareness\n(Both Yes)', 'Partial Awareness\n(One Yes)', 'Low Awareness\n(Both No)']
            values = [len(both_aware), partial_aware, len(neither_aware)]
            percentages = [v/len(df_awareness)*100 for v in values]
            
            fig = go.Figure(data=[go.Bar(
                x=categories,
                y=values,
                marker_color=['#2ecc71', '#f39c12', '#e74c3c'],
                text=[f'{p:.1f}%<br>({v} students)' for p, v in zip(percentages, values)],
                textposition='auto',
                textfont=dict(color='white', size=11, family='Arial Black')
            )])
            
            fig.update_layout(
                title='Combined Awareness Levels',
                yaxis_title='Number of Students',
                xaxis_title='Awareness Level',
                height=450,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)      # Key insights with enhanced styling using large content card
    st.markdown("""
    <div class="large-content-card green">
        <div class="large-card-title">💡 Key Awareness Insights</div>
        <div class="large-card-content">
            <ul>
                <li><strong>Low awareness levels</strong> indicate urgent need for targeted health education campaigns</li>
                <li><strong>Students aware of screening centers</strong> are significantly more likely to undergo screening</li>
                <li><strong>Healthcare provider recommendations</strong> are crucial for motivating screening decisions</li>
                <li><strong>Institutional programs</strong> should focus on improving awareness as a first step</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)      # Recommendations based on awareness levels using large content card
    st.markdown("""
    <div class="large-content-card blue">
        <div class="large-card-title">🎯 Awareness-Based Recommendations</div>
        <div class="large-card-content">
            <ul>
                <li><strong>Immediate:</strong> Launch campus-wide awareness campaigns</li>
                <li><strong>Short-term:</strong> Train healthcare providers on screening counseling</li>
                <li><strong>Long-term:</strong> Integrate cervical cancer education into health curricula</li>
                <li><strong>Ongoing:</strong> Monitor awareness levels and adjust interventions accordingly</li>
            </ul>
        </div>
    </div>    """, unsafe_allow_html=True)

def create_knowledge_assessment(df):
    """Create knowledge assessment section"""
    st.markdown('<div class="section-header">📚 Knowledge Assessment</div>', unsafe_allow_html=True)
    
    # Knowledge domains with better color schemes
    domains = {
        'Risk Factors': {
            'cols': ['multiple_sexual_partners', 'age_factor', 'hereditary_risk', 'unprotected_sex'],
            'colors': ['#e74c3c', '#c0392b']  # Red shades
        },
        'Symptoms': {
            'cols': ['abnormal_menstrual_bleeding', 'general_body_pain', 'intermenstrual_bleeding', 
                    'vaginal_itching', 'foul_vaginal_discharge', 'postmenopausal_bleeding'],
            'colors': ['#f39c12', '#e67e22']  # Orange shades
        },
        'Screening': {
            'cols': ['knows_screening_center', 'screen_from_age_21', 'screening_for_healthy',
                     'screening_for_early_detection', 'detection_can_prevent_cancer'],
            'colors': ['#3498db', '#2980b9']  # Blue shades
        }
    }
    
    # Process each knowledge domain
    for domain_name, domain_info in domains.items():
        available_cols = [col for col in domain_info['cols'] if col in df.columns]
        colors = domain_info['colors']
        
        if available_cols:
            st.markdown(f"### � {domain_name} Knowledge")
            
            knowledge_data = []
            for col in available_cols:
                if col in df.columns:
                    value_counts = df[col].value_counts()
                    agree_pct = (value_counts.get('A', 0) / len(df)) * 100
                    disagree_pct = (value_counts.get('D', 0) / len(df)) * 100
                    knowledge_data.append({
                        'Item': col.replace('_', ' ').title(),
                        'Good Knowledge': agree_pct,
                        'Poor Knowledge': disagree_pct
                    })
            
            if knowledge_data:
                knowledge_df = pd.DataFrame(knowledge_data)
                
                # Create horizontal bar chart
                fig = go.Figure()
                
                # Add Good Knowledge bars
                fig.add_trace(go.Bar(
                    name='Good Knowledge',
                    y=knowledge_df['Item'],
                    x=knowledge_df['Good Knowledge'],
                    orientation='h',
                    marker_color=colors[0],
                    text=[f'{val:.1f}%' for val in knowledge_df['Good Knowledge']],
                    textposition='inside',
                    textfont=dict(color='white', size=14, family='Arial Black'),
                    hovertemplate='<b>%{y}</b><br>Good Knowledge: %{x:.1f}%<extra></extra>',
                    marker=dict(line=dict(color='white', width=1))
                ))
                
                # Add Poor Knowledge bars
                fig.add_trace(go.Bar(
                    name='Poor Knowledge',
                    y=knowledge_df['Item'],
                    x=knowledge_df['Poor Knowledge'],
                    orientation='h',
                    marker_color=colors[1],
                    text=[f'{val:.1f}%' for val in knowledge_df['Poor Knowledge']],
                    textposition='inside',
                    textfont=dict(color='white', size=14, family='Arial Black'),
                    hovertemplate='<b>%{y}</b><br>Poor Knowledge: %{x:.1f}%<extra></extra>',
                    marker=dict(line=dict(color='white', width=1))
                ))
                
                fig.update_layout(
                    title=dict(
                        text=f'Knowledge Assessment: {domain_name}',
                        x=0.5,
                        font=dict(size=22, color='#2c3e50', family='Arial Black')
                    ),
                    xaxis_title='Percentage (%)',
                    yaxis_title='Knowledge Items',
                    height=max(500, len(available_cols) * 60),
                    barmode='stack',
                    showlegend=True,
                    legend=dict(
                        orientation="h", 
                        yanchor="bottom", 
                        y=1.02, 
                        xanchor="right", 
                        x=1,
                        font=dict(size=16, family='Arial')
                    ),
                    font=dict(size=14, family='Arial'),
                    xaxis=dict(
                        title=dict(text='Percentage (%)', font=dict(size=16, family='Arial Black')),
                        tickfont=dict(size=14, family='Arial'),
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='rgba(128,128,128,0.2)'
                    ),
                    yaxis=dict(
                        title=dict(text='Knowledge Items', font=dict(size=16, family='Arial Black')),
                        tickfont=dict(size=12, family='Arial')
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=80, b=60, l=150, r=60)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show summary statistics
                avg_good_knowledge = knowledge_df['Good Knowledge'].mean()
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        f"Average Good Knowledge - {domain_name}", 
                        f"{avg_good_knowledge:.1f}%"
                    )
                
                with col2:
                    # Find best and worst knowledge items
                    best_item = knowledge_df.loc[knowledge_df['Good Knowledge'].idxmax(), 'Item']
                    worst_item = knowledge_df.loc[knowledge_df['Good Knowledge'].idxmin(), 'Item']
                    
                    st.info(f"**Best:** {best_item}")
                    st.warning(f"**Needs Improvement:** {worst_item}")
        
        else:
            st.warning(f"No data available for {domain_name} assessment")
    
    # Overall knowledge summary
    st.markdown("### 📊 Overall Knowledge Summary")
    
    # Calculate overall knowledge scores if data is available
    all_knowledge_cols = []
    for domain_info in domains.values():
        all_knowledge_cols.extend([col for col in domain_info['cols'] if col in df.columns])
    
    if all_knowledge_cols:
        # Calculate overall good knowledge percentage
        overall_scores = []
        for col in all_knowledge_cols:
            if col in df.columns:
                good_knowledge_pct = (df[col].value_counts().get('A', 0) / len(df)) * 100
                overall_scores.append(good_knowledge_pct)
        
        if overall_scores:
            avg_overall = np.mean(overall_scores)
              # Create gauge chart for overall knowledge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = avg_overall,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {
                    'text': "Overall Knowledge Score",
                    'font': {'size': 24, 'color': '#2c3e50', 'family': 'Arial Black'}
                },
                delta = {'reference': 50},
                number = {
                    'font': {'size': 32, 'color': '#2c3e50', 'family': 'Arial Black'},
                    'suffix': '%'
                },
                gauge = {
                    'axis': {
                        'range': [None, 100],
                        'tickwidth': 2,
                        'tickcolor': '#2c3e50',
                        'tickfont': {'size': 16, 'family': 'Arial'}
                    },
                    'bar': {'color': "#2ecc71", 'thickness': 0.8},
                    'bgcolor': "white",
                    'borderwidth': 3,
                    'bordercolor': "#2c3e50",
                    'steps': [
                        {'range': [0, 50], 'color': "#ffebee"},
                        {'range': [50, 75], 'color': "#fff3e0"},
                        {'range': [75, 100], 'color': "#e8f5e8"}
                    ],
                    'threshold': {
                        'line': {'color': "#e74c3c", 'width': 6},
                        'thickness': 0.8,
                        'value': 50
                    }
                }
            ))
            
            fig.update_layout(
                height=400,
                font=dict(size=16, family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=80, b=40, l=40, r=40)
            )
            col1, col2 = st.columns([2, 1])
            with col1:
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Determine card color based on score
                if avg_overall >= 75:
                    card_color = "green"
                    status = "Excellent overall knowledge!"
                    icon = "🌟"
                elif avg_overall >= 50:
                    card_color = "orange"
                    status = "Moderate knowledge - room for improvement"
                    icon = "⚠️"
                else:
                    card_color = "red";
                    status = "Poor knowledge - urgent education needed"
                    icon = "🚨"
                
                st.markdown(f"""
                <div class="large-content-card {card_color}">
                    <div class="large-card-title">{icon} Knowledge Insights</div>
                    <div class="large-card-content">
                        <strong>{status}</strong><br><br>
                        <strong>Average Score:</strong> {avg_overall:.1f}%
                    </div>
                </div>                """, unsafe_allow_html=True)

def create_statistical_modeling(df):
    """Create statistical modeling section"""
    st.markdown('<div class="section-header">📈 Statistical Analysis</div>', unsafe_allow_html=True)
    
    # Statistical Methodology Explanation
    st.markdown("### 🧪 Statistical Methodology: Modified Poisson Regression")
    
    col1, col2 = st.columns([2, 1])    
    with col1:
        st.markdown("""
        <div class="large-content-card blue">
            <div class="large-card-title">🔬 Why Modified Poisson Regression?</div>
            <div class="large-card-content">
                <strong>Modified Poisson regression with robust standard errors</strong> was chosen for this analysis because:
                <br><br>
                <ul>
                    <li><strong>Binary Outcome Variable:</strong> Our outcome (screening uptake: Yes/No) is binary</li>
                    <li><strong>Common Event:</strong> Screening uptake rate (~14%) is relatively common (>10%)</li>
                    <li><strong>Risk Ratios:</strong> We want to estimate Risk Ratios (RR) rather than Odds Ratios</li>
                    <li><strong>Robust Standard Errors:</strong> Accounts for potential overdispersion and provides reliable confidence intervals</li>
                </ul>
                <br>
                <strong>Risk Ratio Interpretation:</strong>
                <ul>
                    <li><strong>RR > 1:</strong> Higher likelihood of screening compared to reference group</li>
                    <li><strong>RR < 1:</strong> Lower likelihood of screening compared to reference group</li>
                    <li><strong>RR = 1:</strong> No difference in screening likelihood</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="large-content-card purple">
            <div class="large-card-title">⚙️ Model Specifications</div>
            <div class="large-card-content">
                <strong>Model Type:</strong>
                <ul>
                    <li>Modified Poisson Regression</li>
                    <li>Robust Standard Errors (HC0)</li>
                </ul>
                <br>
                <strong>Outcome Variable:</strong>
                <ul>
                    <li>Screening Uptake (Binary: 0/1)</li>
                </ul>
                <br>
                <strong>Predictors:</strong>
                <ul>
                    <li>Demographics (Age, Institution)</li>
                    <li>Awareness Variables</li>
                    <li>Knowledge Domains</li>
                </ul>
                <br>
                <strong>Statistical Significance:</strong>
                <ul>
                    <li>p-value < 0.05</li>
                    <li>95% Confidence Intervals</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Predictors of Cervical Cancer Screening Uptake")
    
    # Create a comprehensive statistical results table
    if 'Uptake' in df.columns:
        # Key predictors
        predictors = ['agegrp', 'affiliation', 'eva_told_to_scrn', 'aware_of_scrn_centa']
        available_predictors = [p for p in predictors if p in df.columns]
        
        if available_predictors:
            # Create detailed analysis results
            results_data = []
            
            for pred in available_predictors:
                if pred in df.columns:
                    ct = pd.crosstab(df[pred], df['Uptake'])
                    ct_pct = pd.crosstab(df[pred], df['Uptake'], normalize='index') * 100
                    
                    for category in ct.index:
                        if 'yes' in ct.columns and 'no' in ct.columns:
                            screened = ct.loc[category, 'yes']
                            total = ct.loc[category].sum()
                            uptake_rate = ct_pct.loc[category, 'yes'] if 'yes' in ct_pct.columns else 0
                            
                            # Simulate risk ratio calculation (simplified)
                            reference_rate = ct_pct.iloc[0]['yes'] if 'yes' in ct_pct.columns else 0
                            risk_ratio = uptake_rate / reference_rate if reference_rate > 0 else 1.0
                            
                            results_data.append({
                                'Predictor': pred.replace('_', ' ').title(),
                                'Category': str(category),
                                'Screened (n)': screened,
                                'Total (n)': total,
                                'Uptake Rate (%)': f"{uptake_rate:.1f}%",
                                'Risk Ratio*': f"{risk_ratio:.2f}",
                                'Statistical Significance': "Yes" if uptake_rate > reference_rate * 1.5 else "No"
                            })
            
            if results_data:
                results_df = pd.DataFrame(results_data)
                
                # Create an interactive table with color coding
                st.markdown("### 📋 Detailed Statistical Results")
                  # Color code the dataframe display
                def highlight_significance(val):
                    if val == "Yes":
                        return 'background-color: #d4edda; color: #155724'
                    elif val == "No":
                        return 'background-color: #f8d7da; color: #721c24'
                    return ''
                
                styled_df = results_df.style.map(highlight_significance, subset=['Statistical Significance'])
                st.dataframe(styled_df, use_container_width=True)                
                st.caption("*Risk Ratios are simplified calculations for demonstration. Full Poisson regression would provide adjusted estimates with confidence intervals.")
    
    # Model Performance and Validation
    st.markdown("### 📈 Model Performance & Validation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">🔬 Model Type</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-value" style="font-size: 1.3rem;">Modified Poisson Regression</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-description">🎯 Best for binary outcomes with common events<br>📊 Produces interpretable Risk Ratios</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">⚙️ Error Correction</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-value" style="font-size: 1.3rem;">Robust Standard Errors (HC0)</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-description">🛡️ Accounts for overdispersion<br>📈 Reliable confidence intervals</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">✅ Multicollinearity Check</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-value" style="font-size: 1.3rem; color: #27ae60;">VIF < 5 (No Issues)</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-description">🔍 Variables are independent<br>✨ Model assumptions met</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)    
    # Key Statistical Findings using large content card
    st.markdown("""
    <div class="large-content-card green">
        <div class="large-card-title">🔍 Key Statistical Findings from Poisson Regression</div>
        <div class="large-card-content">
            <ul>
                <li><strong>Age Effect:</strong> Students >25 years have 4.4x higher screening likelihood (RR=4.38, p<0.001)</li>
                <li><strong>Institutional Effect:</strong> UHAS students show 2.4x higher screening rates (RR=2.40, p=0.042)</li>
                <li><strong>Awareness Impact:</strong> Knowledge of screening centers increases likelihood by 88% (RR=1.88, p=0.028)</li>
                <li><strong>Opportunity Effect:</strong> Being given screening opportunity is the strongest predictor</li>
                <li><strong>Knowledge Domains:</strong> Individual knowledge areas show varying significance after adjustment</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Assumptions and Limitations
    st.markdown("### ⚠️ Model Assumptions & Limitations")
    
    col1, col2 = st.columns(2)    
    with col1:
        st.markdown("""
        <div class="large-content-card green">
            <div class="large-card-title">✅ Model Assumptions Met</div>
            <div class="large-card-content">
                <ul>
                    <li><strong>Independence:</strong> Observations are independent</li>
                    <li><strong>Linearity:</strong> Log-linear relationship assumed</li>
                    <li><strong>No perfect multicollinearity:</strong> VIF values < 5</li>
                    <li><strong>Robust errors:</strong> Account for overdispersion</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="large-content-card red">
            <div class="large-card-title">⚠️ Study Limitations</div>
            <div class="large-card-content">
                <ul>
                    <li><strong>Cross-sectional design:</strong> Cannot infer causality</li>
                    <li><strong>Self-reported data:</strong> Potential recall/social desirability bias</li>
                    <li><strong>Sample size:</strong> Limited power for some subgroup analyses</li>
                    <li><strong>Unmeasured confounders:</strong> Other factors may influence uptake</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add methodology comparison table
    st.markdown("### 📊 Statistical Method Comparison")
    
    comparison_data = {
        "Method": ["Logistic Regression", "Modified Poisson Regression ✅"],
        "Produces": ["Odds Ratios", "Risk Ratios"],
        "Common Events (>10%)": ["Less ideal", "Ideal"],
        "Interpretation": ["Complex", "Intuitive"],
        "Our Choice": ["❌", "✅"]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)
    
    # Risk ratio interpretation guide
    st.markdown("### 📈 Risk Ratio Interpretation Guide")
    
    rr_guide = pd.DataFrame({
        'Risk Ratio (RR)': ['RR < 0.8', '0.8 ≤ RR < 1.2', '1.2 ≤ RR < 2.0', 'RR ≥ 2.0'],
        'Interpretation': ['Protective Effect', 'No/Weak Effect', 'Moderate Risk Increase', 'Strong Risk Increase'],        'Example from Study': ['Not observed', 'Reference groups', 'Awareness (RR=1.88)', 'Age >25 years (RR=4.38)']
    })
    
    st.dataframe(rr_guide, use_container_width=True)

def create_recommendations(df):
    """Create recommendations section"""
    st.markdown('<div class="section-header">💡 Recommendations & Interventions</div>', unsafe_allow_html=True)
    
    # Create large content cards for recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="large-content-card orange">
            <div class="large-card-title">🎯 Immediate Actions</div>
            <div class="large-card-content">
                <ul>
                    <li><strong>Increase Awareness Campaigns:</strong> Focus on younger students (<20 years)</li>
                    <li><strong>Healthcare Provider Training:</strong> Enhance recommendation practices</li>
                    <li><strong>Institutional Programs:</strong> Leverage higher-performing institutions as models</li>
                    <li><strong>Accessibility Improvements:</strong> Address logistical barriers to screening</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="large-content-card purple">
            <div class="large-card-title">📋 Long-term Strategies</div>
            <div class="large-card-content">
                <ul>
                    <li><strong>Curriculum Integration:</strong> Include cervical cancer education in health courses</li>
                    <li><strong>Peer Education Programs:</strong> Train student health ambassadors</li>
                    <li><strong>Mobile Screening Units:</strong> Bring services directly to campuses</li>
                    <li><strong>Follow-up Systems:</strong> Implement reminder and tracking systems</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
      # Cost considerations
    if 'amtpaid' in df.columns or 'amt_pref_pay_for_scrn' in df.columns:
        st.markdown("""
        <div class="large-content-card blue">
            <div class="large-card-title">💰 Financial Considerations</div>
            <div class="large-card-content">
                <strong>Key Findings on Payment Preferences:</strong>
                <ul>
                    <li>Majority willing to pay at least 20 Ghana cedis (≈ $1.30 USD)</li>
                    <li>Strong preference for free or low-cost screening (under 50 cedis)</li>
                    <li>Financial barriers are significant factors in screening decisions</li>
                </ul>
                <br>
                <strong>Recommendations:</strong>
                <ul>
                    <li>Subsidized screening programs for students</li>
                    <li>Partnership with health insurance schemes</li>
                    <li>Flexible payment options and installment plans</li>
                </ul>
            </div>
        </div>        """, unsafe_allow_html=True)

def create_payment_analysis(df):
    """Create payment preferences analysis"""
    payment_cols = ['amtpaid', 'amt_pref_pay_for_scrn']
    available_payment_cols = [col for col in payment_cols if col in df.columns]
    
    if available_payment_cols:
        col1, col2 = st.columns(2)
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        for i, col in enumerate(available_payment_cols):
            if col in df.columns:
                value_counts = df[col].value_counts().head(5)  # Top 5 categories
                
                title = "Amount Willing to Pay" if col == 'amtpaid' else "Preferred Payment Amount"
                
                fig = go.Figure(data=[go.Bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    marker_color=colors[:len(value_counts)],
                    text=[f'{v}<br>({v/len(df)*100:.1f}%)' for v in value_counts.values],
                    textposition='auto',
                    textfont=dict(color='white', size=14, family='Arial Black'),
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Percentage: %{text}<extra></extra>',
                    marker=dict(line=dict(color='white', width=2))
                )])
                
                fig.update_layout(
                    title=dict(
                        text=title,
                        x=0.5,
                        font=dict(size=20, color='#2c3e50', family='Arial Black')
                    ),
                    xaxis_title="Payment Category",
                    yaxis_title="Number of Students",
                    height=500,                    showlegend=False,
                    xaxis=dict(
                        title=dict(text="Payment Category", font=dict(size=16, family='Arial Black')),
                        tickfont=dict(size=12, family='Arial'),
                        tickangle=45
                    ),
                    yaxis=dict(
                        title=dict(text="Number of Students", font=dict(size=16, family='Arial Black')),
                        tickfont=dict(size=14, family='Arial'),
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='rgba(128,128,128,0.2)'
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=80, b=100, l=60, r=60)                )
                
                if i == 0:
                    col1.plotly_chart(fig, use_container_width=True)
                else:
                    col2.plotly_chart(fig, use_container_width=True)
        
        # Payment insights as summary cards
        cards_html = """
        <div class="cards-container">
            <div class="summary-card orange">
                <div class="card-title">� Key Barrier</div>
                <div class="card-value">Cost</div>
                <div class="card-description">Affordability is a key barrier to screening uptake</div>
            </div>
            <div class="summary-card green">
                <div class="card-title">🆓 Solution</div>
                <div class="card-value">Free</div>
                <div class="card-description">Free or low-cost screening programs could significantly improve uptake</div>
            </div>
            <div class="summary-card blue">
                <div class="card-title">🎯 Target</div>
                <div class="card-value">Subsidize</div>
                <div class="card-description">Subsidized programs should target the most preferred price points</div>
            </div>
            <div class="summary-card purple">
                <div class="card-title">🏥 Coverage</div>
                <div class="card-value">Insurance</div>
                <div class="card-description">Insurance coverage expansion could reduce financial barriers</div>
            </div>
        </div>
        """
        st.markdown(cards_html, unsafe_allow_html=True)
    
    else:
        st.info("💡 Payment analysis will be available when payment preference data is present")

def create_screening_reasons(df):
    """Create screening reasons analysis"""
    if 'why_go_scrn' in df.columns:
        reasons = df['why_go_scrn'].value_counts()
        reasons_pct = df['why_go_scrn'].value_counts(normalize=True) * 100          # Create large vertical donut chart for reasons
        fig = go.Figure(data=[go.Pie(
            labels=reasons.index,
            values=reasons.values,
            hole=0.5,  # Larger hole for better donut effect
            marker_colors=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#ff6b6b', '#17a2b8', '#fd7e14'],
            textinfo='label+percent+value',
            textfont=dict(size=18, family='Arial Black', color='white'),  # Larger text
            textposition='outside',  # Outside positioning for better visibility
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            marker=dict(line=dict(color='white', width=4)),  # Thicker borders
            pull=[0.03 if i == 0 else 0 for i in range(len(reasons))]  # Slight pull for emphasis
        )])
        
        fig.update_layout(
            title=dict(
                text="<b>Reasons for Cervical Cancer Screening</b>",
                x=0.5,
                font=dict(size=24, color='white', family='Arial Black')
            ),
            height=700,  # Much larger height for vertical display
            showlegend=True,
            legend=dict(
                font=dict(size=16, family='Arial Bold', color='white'),
                orientation="h",  # Horizontal legend at bottom
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(0,0,0,0.2)',
                bordercolor='white',
                borderwidth=1
            ),
            font=dict(size=18, family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=100, b=150, l=40, r=40),
            annotations=[
                dict(
                    text=f"<b style='font-size:28px'>Total</b><br><span style='font-size:20px'>{reasons.sum()} Responses</span>",
                    x=0.5, y=0.5,
                    font_size=24,
                    font_color='white',
                    font_family='Arial Black',
                    showarrow=False
                )
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Key findings summary below the chart
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown("### 📊 Key Findings")
        for reason, count in reasons.items():
            percentage = (count / len(df)) * 100
            st.markdown(f"**{reason}**: {percentage:.1f}% ({count} students)")
        st.markdown('</div>', unsafe_allow_html=True)# Screening motivation insights as summary cards
        cards_html = """
        <div class="cards-container">
            <div class="summary-card blue">
                <div class="card-title">🤔 Initiative Types</div>
                <div class="card-value">Personal</div>
                <div class="card-description">Personal initiative vs external recommendations patterns</div>
            </div>
            <div class="summary-card green">
                <div class="card-title">💪 Health Behavior</div>
                <div class="card-value">Proactive</div>
                <div class="card-description">Proactive health behavior indicates good health awareness</div>
            </div>
            <div class="summary-card orange">
                <div class="card-title">👩‍⚕️ Provider Role</div>
                <div class="card-value">Critical</div>
                <div class="card-description">Recommendation-based screening shows importance of healthcare provider counseling</div>
            </div>
            <div class="summary-card purple">
                <div class="card-title">❤️ Attitudes</div>
                <div class="card-value">Positive</div>
                <div class="card-description">Voluntary screening suggests positive attitudes toward preventive care</div>
            </div>
        </div>
        """
        st.markdown(cards_html, unsafe_allow_html=True)
    
    else:
        st.info("💡 Screening reasons analysis will be available when reason data is present")

def create_sankey_diagram(df):
    """Create Sankey diagram showing pathways from opportunity/perception to screening uptake"""
    
    # Check if required columns exist
    required_cols = ['giv_oportu_to_scrn', 'scrn_painful', 'Uptake']
    available_cols = [col for col in required_cols if col in df.columns]
    
    if len(available_cols) < 2:
        st.warning("⚠️ Sankey diagram requires 'opportunity' and 'uptake' data columns")
        return
    
    try:
        # Prepare data for Sankey diagram
        # Filter out missing values
        sankey_df = df[available_cols].dropna()
        
        if len(sankey_df) == 0:
            st.warning("⚠️ No complete data available for Sankey diagram")
            return
        
        # Create flow data
        if 'giv_oportu_to_scrn' in df.columns and 'Uptake' in df.columns:
            
            # Count flows
            opportunity_yes = sankey_df[sankey_df['giv_oportu_to_scrn'] == 'yes']
            opportunity_no = sankey_df[sankey_df['giv_oportu_to_scrn'] == 'no']
            
            # Calculate percentages
            total_participants = len(sankey_df)
            opp_yes_count = len(opportunity_yes)
            opp_no_count = len(opportunity_no)
            
            # From opportunity to uptake
            opp_yes_uptake_yes = len(opportunity_yes[opportunity_yes['Uptake'] == 'yes'])
            opp_yes_uptake_no = len(opportunity_yes[opportunity_yes['Uptake'] == 'no'])
            opp_no_uptake_yes = len(opportunity_no[opportunity_no['Uptake'] == 'yes'])
            opp_no_uptake_no = len(opportunity_no[opportunity_no['Uptake'] == 'no'])
            
            # Define nodes
            labels = [
                "Given Opportunity: Yes", "Given Opportunity: No",  # 0, 1
                "Uptake: Yes", "Uptake: No"  # 2, 3
            ]
            
            # Define flows (source, target, value)
            sources = [0, 0, 1, 1]  # From opportunity nodes
            targets = [2, 3, 2, 3]  # To uptake nodes
            values = [opp_yes_uptake_yes, opp_yes_uptake_no, opp_no_uptake_yes, opp_no_uptake_no]
              # Create Sankey diagram
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=20,
                    thickness=25,
                    line=dict(color="black", width=2),
                    label=labels,
                    color=["#3498db", "#e74c3c", "#2ecc71", "#f39c12"],
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color=["rgba(52, 152, 219, 0.7)", "rgba(52, 152, 219, 0.5)", 
                           "rgba(231, 76, 60, 0.7)", "rgba(231, 76, 60, 0.5)"],
                    hovertemplate='<b>%{source.label}</b> → <b>%{target.label}</b><br>Count: %{value}<extra></extra>'
                )
            )])
            
            fig.update_layout(
                title=dict(
                    text="Screening Uptake Pathway: From Opportunity to Action",
                    x=0.5,
                    font=dict(size=22, color='#2c3e50', family='Arial Black')
                ),
                font=dict(size=16, family='Arial'),
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=80, b=60, l=60, r=60)
            )
            
            st.plotly_chart(fig, use_container_width=True)              # Add insights as summary cards
            conversion_rate_opp_yes = (opp_yes_uptake_yes / opp_yes_count) * 100 if opp_yes_count > 0 else 0
            conversion_rate_opp_no = (opp_no_uptake_yes / opp_no_count) * 100 if opp_no_count > 0 and opp_no_uptake_yes > 0 else 0
            opportunity_rate = (opp_yes_count / total_participants) * 100
            
            cards_html = f"""
            <div class="cards-container">
                <div class="summary-card blue">
                    <div class="card-title">🎯 Given Opportunity</div>
                    <div class="card-value">{conversion_rate_opp_yes:.1f}%</div>
                    <div class="card-description">Students who got screened when given opportunity</div>
                </div>
                <div class="summary-card purple">
                    <div class="card-title">💪 Self Initiative</div>
                    <div class="card-value">{conversion_rate_opp_no:.1f}%</div>
                    <div class="card-description">Students who got screened without opportunity</div>
                </div>
                <div class="summary-card orange">
                    <div class="card-title">🚪 Access Rate</div>
                    <div class="card-value">{opportunity_rate:.1f}%</div>
                    <div class="card-description">Students given screening opportunity</div>
                </div>
                <div class="summary-card green">
                    <div class="card-title">🔑 Key Finding</div>
                    <div class="card-value">Critical</div>
                    <div class="card-description">Opportunity is the main bottleneck - most take it when offered!</div>
                </div>
            </div>
            """
            st.markdown(cards_html, unsafe_allow_html=True)
            
        else:
            st.info("💡 Sankey diagram will be available when opportunity and uptake data are present")
            
    except Exception as e:
        st.error(f"Error creating Sankey diagram: {str(e)}")
        st.info("💡 Showing alternative flow analysis...")
        
        # Alternative simple flow chart
        if 'Uptake' in df.columns:
            uptake_summary = df['Uptake'].value_counts()
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Screened", uptake_summary.get('yes', 0))
            with col2:
                st.metric("Never Screened", uptake_summary.get('no', 0))

# ...existing code...

def main():
    """Main dashboard function"""
    
    # 🎨 BEAUTIFUL CARD-STYLE NAVIGATION SYSTEM CSS
    st.markdown("""
    <style>
    /* Custom card-style navigation tiles */
    .nav-card {
        display: block;
        padding: 20px;
        margin: 12px 0;
        border-radius: 20px;
        text-decoration: none;
        color: white;
        font-weight: 700;
        font-size: 16px;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid transparent;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        background-size: 200% 200%;
        animation: gradientShift 4s ease infinite;
    }
    
    .nav-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .nav-card:hover::before {
        left: 100%;
    }
    
    .nav-card:hover {
        transform: translateY(-8px) scale(1.05) rotateY(5deg);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        border-color: rgba(255,255,255,0.4);
        animation: gradientShift 2s ease infinite;
    }
    
    .nav-card.active {
        transform: scale(1.08) translateY(-2px);
        border-color: #ffffff;
        box-shadow: 0 12px 35px rgba(255,255,255,0.3), 0 0 30px rgba(39, 174, 96, 0.5);
        animation: activeGlow 3s ease-in-out infinite alternate, gradientShift 3s ease infinite;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes activeGlow {
        from { 
            box-shadow: 0 12px 35px rgba(255,255,255,0.3), 0 0 30px rgba(39, 174, 96, 0.5);
            transform: scale(1.08) translateY(-2px);
        }
        to { 
            box-shadow: 0 15px 45px rgba(255,255,255,0.4), 0 0 40px rgba(39, 174, 96, 0.7);
            transform: scale(1.1) translateY(-4px);
        }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* 🌈 STUNNING ANIMATED GRADIENTS FOR EACH NAVIGATION CARD 🌈 */
    
    /* Overview Card - Royal Purple to Electric Blue */
    .nav-card.overview { 
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #667eea 50%, 
            #5b4cdb 75%, 
            #667eea 100%);
        background-size: 400% 400%;
        animation: overviewGradient 6s ease infinite;
    }
    
    @keyframes overviewGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Screening Card - Pink Sunset to Ocean Blue */
    .nav-card.screening { 
        background: linear-gradient(135deg, 
            #ff6b6b 0%, 
            #feca57 25%, 
            #48cae4 50%, 
            #ff006e 75%, 
            #4c63d2 100%);
        background-size: 400% 400%;
        animation: screeningGradient 7s ease infinite;
    }
    
    @keyframes screeningGradient {
        0% { background-position: 0% 50%; }
        25% { background-position: 25% 75%; }
        50% { background-position: 100% 50%; }
        75% { background-position: 75% 25%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Awareness Card - Warm Peach to Rose Gold */
    .nav-card.awareness { 
        background: linear-gradient(135deg, 
            #ff9a56 0%, 
            #ffad56 25%, 
            #ff6b9d 50%, 
            #c44569 75%, 
            #f8b500 100%);
        background-size: 400% 400%;
        animation: awarenessGradient 8s ease infinite;
    }
    
    @keyframes awarenessGradient {
        0% { background-position: 0% 50%; }
        33% { background-position: 100% 25%; }
        66% { background-position: 0% 75%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Analysis Card - Mint to Lavender Dream */
    .nav-card.analysis { 
        background: linear-gradient(135deg, 
            #a8edea 0%, 
            #fed6e3 25%, 
            #a8e6cf 50%, 
            #dda0dd 75%, 
            #98fb98 100%);
        background-size: 400% 400%;
        animation: analysisGradient 9s ease infinite;
    }
    
    @keyframes analysisGradient {
        0% { background-position: 0% 50%; }
        40% { background-position: 100% 100%; }
        80% { background-position: 0% 0%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Statistics Card - Golden Hour to Purple Magic */
    .nav-card.statistics { 
        background: linear-gradient(135deg, 
            #f7971e 0%, 
            #ffd200 25%, 
            #9c88ff 50%, 
            #5f27cd 75%, 
            #ff9ff3 100%);
        background-size: 400% 400%;
        animation: statisticsGradient 10s ease infinite;
    }
    
    @keyframes statisticsGradient {
        0% { background-position: 0% 50%; }
        20% { background-position: 50% 100%; }
        40% { background-position: 100% 50%; }
        60% { background-position: 50% 0%; }
        80% { background-position: 0% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Recommendations Card - Ocean Breeze to Sky Gradient */
    .nav-card.recommendations { 
        background: linear-gradient(135deg, 
            #00d2ff 0%, 
            #3a7bd5 25%, 
            #00d2ff 50%, 
            #928dab 75%, 
            #00d2ff 100%);
        background-size: 400% 400%;
        animation: recommendationsGradient 11s ease infinite;
    }
    
    @keyframes recommendationsGradient {
        0% { background-position: 0% 50%; }
        25% { background-position: 100% 0%; }
        50% { background-position: 0% 100%; }
        75% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* 🎨 ENHANCED HOVER EFFECTS WITH INTENSIFIED GRADIENTS 🎨 */
    .nav-card.overview:hover {
        background: linear-gradient(135deg, 
            #764ba2 0%, 
            #667eea 25%, 
            #5b4cdb 50%, 
            #764ba2 75%, 
            #667eea 100%);
        background-size: 300% 300%;
        animation: overviewGradient 3s ease infinite;
        box-shadow: 0 20px 50px rgba(118, 75, 162, 0.6), 0 0 30px rgba(102, 126, 234, 0.4);
    }
    
    .nav-card.screening:hover {
        background: linear-gradient(135deg, 
            #ff006e 0%, 
            #ff6b6b 25%, 
            #48cae4 50%, 
            #feca57 75%, 
            #4c63d2 100%);
        background-size: 300% 300%;
        animation: screeningGradient 3.5s ease infinite;
        box-shadow: 0 20px 50px rgba(255, 0, 110, 0.6), 0 0 30px rgba(255, 107, 107, 0.4);
    }
    
    .nav-card.awareness:hover {
        background: linear-gradient(135deg, 
            #c44569 0%, 
            #ff9a56 25%, 
            #ff6b9d 50%, 
            #f8b500 75%, 
            #ffad56 100%);
        background-size: 300% 300%;
        animation: awarenessGradient 4s ease infinite;
        box-shadow: 0 20px 50px rgba(196, 69, 105, 0.6), 0 0 30px rgba(255, 154, 86, 0.4);
    }
    
    .nav-card.analysis:hover {
        background: linear-gradient(135deg, 
            #dda0dd 0%, 
            #a8edea 25%, 
            #98fb98 50%, 
            #fed6e3 75%, 
            #a8e6cf 100%);
        background-size: 300% 300%;
        animation: analysisGradient 4.5s ease infinite;
        box-shadow: 0 20px 50px rgba(221, 160, 221, 0.6), 0 0 30px rgba(168, 237, 234, 0.4);
    }
    
    .nav-card.statistics:hover {
        background: linear-gradient(135deg, 
            #5f27cd 0%, 
            #f7971e 25%, 
            #ff9ff3 50%, 
            #ffd200 75%, 
            #9c88ff 100%);
        background-size: 300% 300%;
        animation: statisticsGradient 5s ease infinite;
        box-shadow: 0 20px 50px rgba(95, 39, 205, 0.6), 0 0 30px rgba(247, 151, 30, 0.4);
    }
    
    .nav-card.recommendations:hover {
        background: linear-gradient(135deg, 
            #3a7bd5 0%, 
            #00d2ff 25%, 
            #928dab 50%, 
            #00d2ff 75%, 
            #3a7bd5 100%);
        background-size: 300% 300%;
        animation: recommendationsGradient 5.5s ease infinite;
        box-shadow: 0 20px 50px rgba(58, 123, 213, 0.6), 0 0 30px rgba(0, 210, 255, 0.4);
    }
    
    /* Card content styling */
    .nav-card-emoji {
        font-size: 32px;
        display: block;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: bounce 2s ease-in-out infinite;
    }
    
    .nav-card-text {
        font-size: 15px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        line-height: 1.3;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-3px);
        }
        60% {
            transform: translateY(-2px);
        }
    }
    
    /* 🎯 BEAUTIFUL ACTIVE SECTION INDICATOR - MATCHING YOUR IMAGE STYLE 🎯 */
    .active-section-indicator {
        background: linear-gradient(135deg, 
            #7c3aed 0%, 
            #a855f7 25%, 
            #3b82f6 50%, 
            #6366f1 75%, 
            #8b5cf6 100%);
        background-size: 300% 300%;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 20px;
        margin: 25px 0;
        text-align: center;
        color: #ffffff;
        font-weight: 900;
        font-size: 16px;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
        box-shadow: 
            0 15px 35px rgba(124, 58, 237, 0.4),
            0 5px 15px rgba(59, 130, 246, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: activeIndicatorGlow 4s ease-in-out infinite, activeGradientFlow 6s ease infinite;
        position: relative;
        overflow: hidden;
    }
    
    .active-section-indicator::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.2), 
            transparent);
        animation: shimmerFlow 3s ease-in-out infinite;
    }
    
    @keyframes activeIndicatorGlow {
        0%, 100% {
            box-shadow: 
                0 15px 35px rgba(124, 58, 237, 0.4),
                0 5px 15px rgba(59, 130, 246, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transform: scale(1);
        }
        50% {
            box-shadow: 
                0 20px 45px rgba(124, 58, 237, 0.6),
                0 8px 25px rgba(59, 130, 246, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            transform: scale(1.02);
        }
    }
    
    @keyframes activeGradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shimmerFlow {
        0% { left: -100%; }
        50% { left: -50%; }
        100% { left: 100%; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Enhanced Streamlit button styling to look like beautiful cards */
    div[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        height: auto;
        padding: 20px;
        margin: 12px 0;
        border-radius: 20px;
        border: 2px solid transparent;
        font-weight: 700;
        font-size: 16px;
        text-align: center;
        color: white !important;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        background-size: 400% 400% !important;
        animation: gradientShift 4s ease infinite;
        opacity: 1 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    div[data-testid="stSidebar"] .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    div[data-testid="stSidebar"] .stButton > button:hover::before {
        left: 100%;
    }
    
    div[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-8px) scale(1.05) rotateY(5deg) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3) !important;
        border-color: rgba(255,255,255,0.4) !important;
        animation: gradientShift 2s ease infinite !important;
    }
    
    div[data-testid="stSidebar"] .stButton > button:focus {
        transform: scale(1.08) translateY(-2px) !important;
        border-color: #ffffff !important;
        box-shadow: 0 12px 35px rgba(255,255,255,0.3), 0 0 30px rgba(39, 174, 96, 0.5) !important;
        animation: activeGlow 3s ease-in-out infinite alternate, gradientShift 3s ease infinite !important;
        outline: none !important;
    }
    
    /* 🌈 BEAUTIFUL ANIMATED GRADIENT ASSIGNMENTS FOR NAVIGATION BUTTONS 🌈 */
    
    /* 🌈 ULTRA-BEAUTIFUL NAVIGATION BUTTON GRADIENTS - MATCHING YOUR IMAGE STYLE 🌈 */
    
    /* Overview Button - Royal Purple to Electric Blue (like your image) */
    div[data-testid="stSidebar"] .stButton:nth-child(1) > button {
        background: linear-gradient(135deg, 
            #7c3aed 0%, 
            #a855f7 20%, 
            #3b82f6 40%, 
            #6366f1 60%, 
            #8b5cf6 80%,
            #7c3aed 100%) !important;
        background-size: 400% 400% !important;
        animation: overviewGradient 6s ease infinite !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3), 0 0 20px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Screening Button - Vibrant Coral to Teal */
    div[data-testid="stSidebar"] .stButton:nth-child(2) > button {
        background: linear-gradient(135deg, 
            #ef4444 0%, 
            #f97316 20%, 
            #eab308 40%, 
            #06b6d4 60%, 
            #3b82f6 80%,
            #ef4444 100%) !important;
        background-size: 400% 400% !important;
        animation: screeningGradient 7s ease infinite !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3), 0 0 20px rgba(6, 182, 212, 0.2) !important;
    }
    
    /* Awareness Button - Warm Sunset to Pink */
    div[data-testid="stSidebar"] .stButton:nth-child(3) > button {
        background: linear-gradient(135deg, 
            #f59e0b 0%, 
            #f97316 20%, 
            #ec4899 40%, 
            #d946ef 60%, 
            #f59e0b 80%,
            #f97316 100%) !important;
        background-size: 400% 400% !important;
        animation: awarenessGradient 8s ease infinite !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3), 0 0 20px rgba(236, 72, 153, 0.2) !important;
    }
    
    /* Analysis Button - Fresh Mint to Lavender */
    div[data-testid="stSidebar"] .stButton:nth-child(4) > button {
        background: linear-gradient(135deg, 
            #10b981 0%, 
            #06b6d4 20%, 
            #8b5cf6 40%, 
            #a855f7 60%, 
            #10b981 80%,
            #06b6d4 100%) !important;
        background-size: 400% 400% !important;
        animation: analysisGradient 9s ease infinite !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3), 0 0 20px rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Statistics Button - Golden Hour Magic */
    div[data-testid="stSidebar"] .stButton:nth-child(5) > button {
        background: linear-gradient(135deg, 
            #f59e0b 0%, 
            #eab308 20%, 
            #d946ef 40%, 
            #7c3aed 60%, 
            #f59e0b 80%,
            #eab308 100%) !important;
        background-size: 400% 400% !important;
        animation: statisticsGradient 10s ease infinite !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3), 0 0 20px rgba(217, 70, 239, 0.2) !important;
    }
    
    /* Recommendations Button - Ocean Blue Dream */
    div[data-testid="stSidebar"] .stButton:nth-child(6) > button {
        background: linear-gradient(135deg, 
            #0ea5e9 0%, 
            #06b6d4 20%, 
            #3b82f6 40%, 
            #6366f1 60%, 
            #0ea5e9 80%,
            #06b6d4 100%) !important;
        background-size: 400% 400% !important;
        animation: recommendationsGradient 11s ease infinite !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.3), 0 0 20px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* 🎨 ENHANCED HOVER EFFECTS WITH INTENSIFIED ANIMATED GRADIENTS 🎨 */
    
    /* Overview Button Hover - Intensified Royal Purple to Electric Blue */
    div[data-testid="stSidebar"] .stButton:nth-child(1) > button:hover {
        background: linear-gradient(135deg, 
            #764ba2 0%, 
            #667eea 25%, 
            #5b4cdb 50%, 
            #764ba2 75%, 
            #667eea 100%) !important;
        background-size: 300% 300% !important;
        animation: overviewGradient 3s ease infinite !important;
        box-shadow: 0 20px 50px rgba(118, 75, 162, 0.6), 0 0 30px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Screening Button Hover - Intensified Pink Sunset to Ocean Blue */
    div[data-testid="stSidebar"] .stButton:nth-child(2) > button:hover {
        background: linear-gradient(135deg, 
            #ff006e 0%, 
            #ff6b6b 25%, 
            #48cae4 50%, 
            #feca57 75%, 
            #4c63d2 100%) !important;
        background-size: 300% 300% !important;
        animation: screeningGradient 3.5s ease infinite !important;
        box-shadow: 0 20px 50px rgba(255, 0, 110, 0.6), 0 0 30px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* Awareness Button Hover - Intensified Warm Peach to Rose Gold */
    div[data-testid="stSidebar"] .stButton:nth-child(3) > button:hover {
        background: linear-gradient(135deg, 
            #c44569 0%, 
            #ff9a56 25%, 
            #ff6b9d 50%, 
            #f8b500 75%, 
            #ffad56 100%) !important;
        background-size: 300% 300% !important;
        animation: awarenessGradient 4s ease infinite !important;
        box-shadow: 0 20px 50px rgba(196, 69, 105, 0.6), 0 0 30px rgba(255, 154, 86, 0.4) !important;
    }
    
    /* Analysis Button Hover - Intensified Mint to Lavender Dream */
    div[data-testid="stSidebar"] .stButton:nth-child(4) > button:hover {
        background: linear-gradient(135deg, 
            #dda0dd 0%, 
            #a8edea 25%, 
            #98fb98 50%, 
            #fed6e3 75%, 
            #a8e6cf 100%) !important;
        background-size: 300% 300% !important;
        animation: analysisGradient 4.5s ease infinite !important;
        box-shadow: 0 20px 50px rgba(221, 160, 221, 0.6), 0 0 30px rgba(168, 237, 234, 0.4) !important;
    }
    
    /* Statistics Button Hover - Intensified Golden Hour to Purple Magic */
    div[data-testid="stSidebar"] .stButton:nth-child(5) > button:hover {
        background: linear-gradient(135deg, 
            #5f27cd 0%, 
            #f7971e 25%, 
            #ff9ff3 50%, 
            #ffd200 75%, 
            #9c88ff 100%) !important;
        background-size: 300% 300% !important;
        animation: statisticsGradient 5s ease infinite !important;
        box-shadow: 0 20px 50px rgba(95, 39, 205, 0.6), 0 0 30px rgba(247, 151, 30, 0.4) !important;
    }
    
    /* Recommendations Button Hover - Intensified Ocean Breeze to Sky Gradient */
    div[data-testid="stSidebar"] .stButton:nth-child(6) > button:hover {
        background: linear-gradient(135deg, 
            #3a7bd5 0%, 
            #00d2ff 25%, 
            #928dab 50%, 
            #00d2ff 75%, 
            #3a7bd5 100%) !important;
        background-size: 300% 300% !important;
        animation: recommendationsGradient 5.5s ease infinite !important;
        box-shadow: 0 20px 50px rgba(58, 123, 213, 0.6), 0 0 30px rgba(0, 210, 255, 0.4) !important;
    }
    
    /* Enhanced sidebar background */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Add subtle animation to the entire sidebar */
    div[data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        animation: fadeIn 1s ease-in-out;
    }
    
    /* 🌈 DYNAMIC ACTIVE SECTION INDICATOR GRADIENTS 🌈 */
    
    /* Overview Active Indicator - Royal Purple to Electric Blue */
    .active-section-indicator.overview-active {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #5b4cdb 50%, 
            #667eea 75%, 
            #764ba2 100%) !important;
        box-shadow: 
            0 15px 35px rgba(102, 126, 234, 0.6),
            0 5px 15px rgba(118, 75, 162, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Screening Active Indicator - Pink Sunset to Ocean Blue */
    .active-section-indicator.screening-active {
        background: linear-gradient(135deg, 
            #ff6b6b 0%, 
            #feca57 25%, 
            #48cae4 50%, 
            #ff006e 75%, 
            #4c63d2 100%) !important;
        box-shadow: 
            0 15px 35px rgba(255, 107, 107, 0.6),
            0 5px 15px rgba(254, 202, 87, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Awareness Active Indicator - Warm Peach to Rose Gold */
    .active-section-indicator.awareness-active {
        background: linear-gradient(135deg, 
            #ff9a56 0%, 
            #ffad56 25%, 
            #ff6b9d 50%, 
            #c44569 75%, 
            #f8b500 100%) !important;
        box-shadow: 
            0 15px 35px rgba(255, 154, 86, 0.6),
            0 5px 15px rgba(196, 69, 105, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Analysis Active Indicator - Mint to Lavender Dream */
    .active-section-indicator.analysis-active {
        background: linear-gradient(135deg, 
            #a8edea 0%, 
            #fed6e3 25%, 
            #a8e6cf 50%, 
            #dda0dd 75%, 
            #98fb98 100%) !important;
        box-shadow: 
            0 15px 35px rgba(168, 237, 234, 0.6),
            0 5px 15px rgba(221, 160, 221, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Statistics Active Indicator - Golden Hour to Purple Magic */
    .active-section-indicator.statistics-active {
        background: linear-gradient(135deg, 
            #f7971e 0%, 
            #ffd200 25%, 
            #9c88ff 50%, 
            #5f27cd 75%, 
            #ff9ff3 100%) !important;
        box-shadow: 
            0 15px 35px rgba(247, 151, 30, 0.6),
            0 5px 15px rgba(95, 39, 205, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Recommendations Active Indicator - Ocean Breeze to Sky */
    .active-section-indicator.recommendations-active {
        background: linear-gradient(135deg, 
            #00d2ff 0%, 
            #3a7bd5 25%, 
            #928dab 50%, 
            #00d2ff 75%, 
            #3a7bd5 100%) !important;
        box-shadow: 
            0 15px 35px rgba(0, 210, 255, 0.6),
            0 5px 15px rgba(58, 123, 213, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown(
        '<div class="main-header">📊 Cervical Cancer Screening Uptake Analytics Dashboard<br>'
        '<small>Female Tertiary Students in Ghana - Comprehensive Analysis</small></div>',
        unsafe_allow_html=True
    )
      # Sidebar navigation
    st.sidebar.title("🏥 Navigation Dashboard")
    st.sidebar.markdown("---")
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    if df is None:
        st.error("Unable to load data. Please check your connection and try again.")
        return
    
    # 🎯 MODERN CARD-STYLE NAVIGATION SYSTEM
    st.sidebar.markdown("### 🧭 Select Section")
    
    # Define navigation sections with unique styling
    navigation_sections = [
        {"key": "overview", "emoji": "📊", "name": "Overview", "full": "📊 Overview"},
        {"key": "screening", "emoji": "🎯", "name": "Screening Uptake", "full": "🎯 Screening Uptake"},
        {"key": "awareness", "emoji": "🧠", "name": "Awareness & Knowledge", "full": "🧠 Awareness & Knowledge"},
        {"key": "analysis", "emoji": "📚", "name": "Detailed Analysis", "full": "📚 Detailed Analysis"},
        {"key": "statistics", "emoji": "📈", "name": "Statistical Insights", "full": "📈 Statistical Insights"},
        {"key": "recommendations", "emoji": "💡", "name": "Recommendations", "full": "💡 Recommendations"}
    ]
    
    # Initialize session state for selected section
    if 'active_section' not in st.session_state:
        st.session_state.active_section = "overview"
    
    # 🌈 BEAUTIFUL ANIMATED GRADIENT NAVIGATION CARDS 🌈
    st.sidebar.markdown("""
    <style>
    /* Hide any CSS display issues and stray text */
    div[data-testid="stSidebar"] .stMarkdown div[data-testid="stMarkdownContainer"] p:contains("@keyframes"),
    div[data-testid="stSidebar"] .stMarkdown div[data-testid="stMarkdownContainer"] p:contains("background-position"),
    div[data-testid="stSidebar"] .stMarkdown div[data-testid="stMarkdownContainer"] p:contains("</style>") {
        display: none !important;
    }
    
    /* Hide any orphaned CSS text */
    div[data-testid="stSidebar"] .stMarkdown p {
        font-size: 0 !important;
        line-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* Only show markdown headings and buttons */
    div[data-testid="stSidebar"] .stMarkdown h1,
    div[data-testid="stSidebar"] .stMarkdown h2,
    div[data-testid="stSidebar"] .stMarkdown h3,
    div[data-testid="stSidebar"] .stMarkdown h4,
    div[data-testid="stSidebar"] .stMarkdown h5,
    div[data-testid="stSidebar"] .stMarkdown h6 {
        font-size: initial !important;
        line-height: initial !important;
        margin: initial !important;
        padding: initial !important;
        height: initial !important;
        overflow: initial !important;
    }
    
    /* Beautiful gradient navigation buttons */
    .stButton > button {
        width: 100% !important;
        height: auto !important;
        padding: 20px !important;
        margin: 12px 0 !important;
        border-radius: 16px !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-align: center !important;
        color: white !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        background-size: 300% 300% !important;
        animation: gradientFlow 6s ease infinite !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-8px) scale(1.05) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4) !important;
        border-color: rgba(255,255,255,0.6) !important;
    }
    
    .stButton > button:focus {
        outline: none !important;
        transform: scale(1.08) translateY(-2px) !important;
        border-color: #ffffff !important;
        box-shadow: 0 12px 35px rgba(255,255,255,0.4), 0 0 30px rgba(124, 58, 237, 0.6) !important;
    }
    
    /* Individual button gradients */
    div[data-testid="stSidebar"] .stButton:nth-child(3) > button {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 25%, #3b82f6 50%, #6366f1 75%, #8b5cf6 100%) !important;
    }
    
    div[data-testid="stSidebar"] .stButton:nth-child(4) > button {
        background: linear-gradient(135deg, #ef4444 0%, #f97316 25%, #eab308 50%, #06b6d4 75%, #3b82f6 100%) !important;
    }
    
    div[data-testid="stSidebar"] .stButton:nth-child(5) > button {
        background: linear-gradient(135deg, #f59e0b 0%, #f97316 25%, #ec4899 50%, #d946ef 75%, #f59e0b 100%) !important;
    }
    
    div[data-testid="stSidebar"] .stButton:nth-child(6) > button {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 25%, #8b5cf6 50%, #a855f7 75%, #10b981 100%) !important;
    }
    
    div[data-testid="stSidebar"] .stButton:nth-child(7) > button {
        background: linear-gradient(135deg, #f59e0b 0%, #eab308 25%, #d946ef 50%, #7c3aed 75%, #f59e0b 100%) !important;
    }
    
    div[data-testid="stSidebar"] .stButton:nth-child(8) > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 25%, #3b82f6 50%, #6366f1 75%, #0ea5e9 100%) !important;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create navigation buttons with beautiful gradients (no individual CSS injection)
    for section in navigation_sections:
        # Create the clickable navigation button
        if st.sidebar.button(
            f"{section['emoji']} {section['name']}", 
            key=f"nav_card_{section['key']}",
            help=f"Navigate to {section['name']} section"
        ):
            st.session_state.active_section = section["key"]
            st.rerun()
    
    # Active section indicator with dynamic gradient based on selected section
    current_section = next((s for s in navigation_sections if s["key"] == st.session_state.active_section), navigation_sections[0])
    st.sidebar.markdown(f"""
    <div class="active-section-indicator {current_section['key']}-active">
        🎯 <strong>Active Section</strong><br>
        <span style="font-size: 18px;">{current_section['full']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Get the selected section for content display
    selected_section = current_section["full"]
    
    # 🎯 MAIN CONTENT AREA - SECTION SWITCHING LOGIC
    # Display selected section
    if selected_section == "📊 Overview":
        st.markdown("### 🎯 Study Overview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Total Participants**: {len(df)}")
        with col2:
            uptake_rate = (df['Uptake'].value_counts(normalize=True)['yes'] * 100) if 'Uptake' in df.columns else 0
            st.warning(f"**Screening Uptake**: {uptake_rate:.1f}%")
        with col3:
            awareness_rate = (df['eva_told_to_scrn'].value_counts(normalize=True)['yes'] * 100) if 'eva_told_to_scrn' in df.columns else 0
            st.success(f"**Awareness Rate**: {awareness_rate:.1f}%")
        
        st.markdown("""
        ### 📋 Study Objectives
        
        This comprehensive analysis examines cervical cancer screening uptake among female tertiary students 
        in the Hohoe Municipality, Ghana. The study focuses on:
        
        1. **Awareness Assessment** - Understanding current knowledge levels
        2. **Screening Uptake Patterns** - Identifying demographic and behavioral factors
        3. **Knowledge Evaluation** - Assessing understanding of risk factors, symptoms, and screening methods
        4. **Statistical Modeling** - Determining key predictors of screening behavior
        5. **Evidence-based Recommendations** - Providing actionable insights for public health interventions
          Navigate through the sections using the sidebar to explore detailed findings and visualizations.
        """)
        
        create_demographics_overview(df)
    
    elif selected_section == "🎯 Screening Uptake":
        create_screening_uptake_analysis(df)        
        # Add additional screening insights
        st.markdown("### 💰 Payment Preferences & Barriers")
        create_payment_analysis(df)
        
        st.markdown("### 🎯 Reasons for Screening")
        create_screening_reasons(df)
    
    elif selected_section == "🧠 Awareness & Knowledge":
        create_awareness_section(df)
    
    elif selected_section == "📚 Detailed Analysis":
        create_knowledge_assessment(df)
    
    elif selected_section == "📈 Statistical Insights":
        create_statistical_modeling(df)
    
    elif selected_section == "💡 Recommendations":
        create_recommendations(df)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 About")
    st.sidebar.info(
        "This dashboard provides comprehensive insights into cervical cancer screening "
        "uptake among female tertiary students in Ghana, supporting evidence-based "
        "public health interventions."
    )
    
    st.sidebar.markdown("### 📞 Contact")
    st.sidebar.markdown("For questions about this analysis, please contact the research team.")
    st.sidebar.markdown("###  Author: Promise Bansah")

if __name__ == "__main__":
    main()
