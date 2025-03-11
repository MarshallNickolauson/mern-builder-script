import os
import subprocess
import json

def run_command(command):
    """Run a shell command and wait for it to complete."""
    process = subprocess.run(command, shell=True, check=True)
    return process.returncode

def create_backend(project_name):
    """Function to set up the backend."""
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)
    
    # Initialize root package.json for concurrently
    run_command("npm init -y")
    run_command("npm i --save-dev concurrently")
    
    with open("package.json", "r") as main_package_file:
        main_package_json = json.load(main_package_file)
    
    main_package_json['scripts'] = {
        "server": "npm run server --prefix backend",
        "client": "npm run dev --prefix frontend",
        "dev": "concurrently \"npm run server\" \"npm run client\""
    }
    
    with open("package.json", "w") as main_package_file:
        json.dump(main_package_json, main_package_file, indent=2)
    
    # Setup backend
    os.makedirs("backend", exist_ok=True)
    os.chdir("backend")
    
    run_command("npm init -y")
    run_command("npm i express dotenv mongoose colors cors express-async-handler bcryptjs jsonwebtoken cookie-parser")
    run_command("npm i --save-dev nodemon")
    
    with open("package.json", "r") as backend_package_file:
        backend_package_json = json.load(backend_package_file)
    
    backend_package_json['scripts'] = {
        "start": "node server.js",
        "server": "nodemon server.js"
    }
    backend_package_json['type'] = "module"
    
    with open("package.json", "w") as backend_package_file:
        json.dump(backend_package_json, backend_package_file, indent=2)
    
    # Create backend files
    with open(".gitignore", "w") as gitignore_file:
        gitignore_file.write("node_modules\n.env\n")
    
    with open(".env", "w") as env_file:
        env_file.write(f"""
NODE_ENV=development
BACKEND_PORT=5000
MONGO_URI=mongodb://localhost:27017/{project_name}
JWT_SECRET=jwtSecret123
""")
    
    os.makedirs("config", exist_ok=True)
    os.makedirs("controllers", exist_ok=True)
    os.makedirs("middleware", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("routes", exist_ok=True)
    
    with open("server.js", "w") as server_file:
        server_file.write("""
import express from 'express';
import cookieParser from 'cookie-parser';
import { errorHandler } from './middleware/errorMiddleware.js';
import { connectDB } from './config/db.js';
import cors from 'cors';
import dotenv from 'dotenv';
dotenv.config();
const port = process.env.BACKEND_PORT || 5000;

connectDB();

const app = express();

if (process.env.NODE_ENV === 'development') {
    app.use(cors({
        origin: 'http://localhost:3000',
        credentials: true
    }));
}

app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// app.use('/route', importedRoute)

app.use(errorHandler);

app.listen(port, () => console.log(`Server started on port ${port}`));
""")
    
    with open("middleware/errorMiddleware.js", "w") as middleware_file:
        middleware_file.write("""
export const errorHandler = (err, req, res, next) => {
    const statusCode = res.statusCode ? res.statusCode : 500;
    res.status(statusCode);
    res.json({
        message: err.message,
        stack: process.env.NODE_ENV === 'production' ? null : err.stack
    });
};
""")
    
    with open("config/db.js", "w") as db_file:
        db_file.write("""
import mongoose from 'mongoose';
import colors from 'colors';

export const connectDB = async () => {
    try {
        const conn = await mongoose.connect(process.env.MONGO_URI);
        console.log(`MongoDB Connected: ${conn.connection.host}`.cyan.underline);
    } catch (error) {
        console.log(error);
        console.log("Add Mongo URI to .env!".red);
        console.log("(Add JWT secret too)".red);
        process.exit(1);
    }
};
""")
    
    print(f"Backend setup complete for project: {project_name}")
    os.chdir("..")

from mern_frontend_builder import MernFrontendBuilder

if __name__ == "__main__":
    project_name = input("Enter your project name: ")
    create_backend(project_name)
    
    frontendBuilder = MernFrontendBuilder()
    frontendBuilder.create_react_app()
    
    print("Starting the development server...")
    subprocess.Popen("npm run dev", shell=True)
    
    print(f"Project {project_name} setup complete with backend and frontend!")
