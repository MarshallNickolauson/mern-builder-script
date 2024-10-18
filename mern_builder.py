import os
import subprocess
import webbrowser
import time
import json

def run_command(command):
    """Run a shell command and wait for it to complete."""
    process = subprocess.run(command, shell=True, check=True)
    return process.returncode

def create_backend(project_name):
    """Function to set up the backend."""
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

    # Install backend dependencies
    run_command("npm init -y")
    run_command("npm i express dotenv mongoose colors cors express-async-handler bcryptjs jsonwebtoken")
    run_command("npm i --save-dev concurrently nodemon")

    # Modify the package.json file for scripts
    with open("package.json", "r") as package_file:
        package_json = json.load(package_file)

    package_json['scripts'] = {
        "start": "node backend/server.js",
        "server": "nodemon backend/server.js",
        "client": "npm run dev --prefix frontend",
        "dev": 'concurrently "npm run server" "npm run client"'
    }

    with open("package.json", "w") as package_file:
        json.dump(package_json, package_file, indent=2)

    # Create a .gitignore file
    with open(".gitignore", "w") as gitignore_file:
        gitignore_file.write("node_modules\n.env\n")

    # Create a .env file
    with open(".env", "w") as env_file:
        env_file.write("""\
NODE_ENV=development
BACKEND_PORT=5000
MONGO_URI=
JWT_SECRET=
""")

    # Create backend folder structure
    os.makedirs("backend/config", exist_ok=True)
    os.makedirs("backend/controllers", exist_ok=True)
    os.makedirs("backend/middleware", exist_ok=True)
    os.makedirs("backend/models", exist_ok=True)
    os.makedirs("backend/routes", exist_ok=True)

    # Create server.js file
    server_js_content = """\
import express from 'express';
import { errorHandler } from './middleware/errorMiddleware.js';
import { connectDB } from './config/db.js';
import cors from 'cors';
import dotenv from 'dotenv';
dotenv.config();
const port = process.env.BACKEND_PORT || 5000;

connectDB();

const app = express();

if (process.env.NODE_ENV === 'development') {
    app.use(cors());
}

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// app.use('/route', importedRoute)

app.use(errorHandler);

app.listen(port, () => console.log(`Server started on port ${port}`));
"""
    with open("backend/server.js", "w") as server_file:
        server_file.write(server_js_content)

    # Create errorMiddleware.js
    error_middleware_content = """\
export const errorHandler = (err, req, res, next) => {
    const statusCode = res.statusCode ? res.statusCode : 500;
    res.status(statusCode);
    res.json({
        message: err.message,
        stack: process.env.NODE_ENV === 'production' ? null : err.stack
    })
}
"""
    with open("backend/middleware/errorMiddleware.js", "w") as middleware_file:
        middleware_file.write(error_middleware_content)

    print(f"Backend setup complete for project: {project_name}")

def create_react_app():
    """Function to set up the frontend React app inside the project folder."""

    # Step 1: Create frontend directory
    frontend_dir = "frontend"
    os.makedirs(frontend_dir, exist_ok=True)
    os.chdir(frontend_dir)

    # Step 2: Create Vite React app
    print(f"Creating Vite React app in {frontend_dir}...")
    run_command(f"npm create vite@latest . -- --template react")

    # Step 3: Install required packages
    print("Installing dependencies...")
    run_command("npm install react-icons react-redux @reduxjs/toolkit tailwindcss postcss autoprefixer react-router-dom react-spinners react-toastify axios")
    run_command("npm install --save-dev jest @testing-library/react @testing-library/jest-dom redux-mock-store redux-thunk axios-mock-adapter babel-jest @babel/preset-env @babel/preset-react jest-fetch-mock")

    # Step 4: Initialize Tailwind CSS
    run_command("npx tailwindcss init -p")

    # Add the rest of your frontend modifications here (like Tailwind config, Vite config, etc.)
    # All the code blocks you've written (App.jsx, store.js, main.jsx, index.html) can be included here.

    # Example of modifying a file (as you did in your other script):
    # Modify the tailwind.config.js file
    tailwind_config_content = """\
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors can go here
      },
      fontFamily: {
        roboto: ['Roboto', 'sans-serif'],
        ropa: ['Ropa Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
"""
    with open("tailwind.config.js", "w") as tailwind_file:
        tailwind_file.write(tailwind_config_content)
    print("Updated tailwind.config.js")

    # (Continue adding all other steps to set up your React app)
    print("Frontend React app setup complete.")

if __name__ == "__main__":
    project_name = input("Enter your project name: ")

    # Step 1: Create backend
    create_backend(project_name)

    # Step 2: Create frontend in the same project folder
    create_react_app()

    print(f"Project {project_name} setup complete with backend and frontend!")
