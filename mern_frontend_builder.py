import os
import subprocess
import webbrowser
import time
import json

def run_command(command):
    """Run a shell command and wait for it to complete."""
    process = subprocess.run(command, shell=True, check=True)
    return process.returncode

class MernFrontendBuilder():
  def __init__(self):
      pass

  def create_react_app(self):
    project_name = "frontend"

    # Step 1: Create Vite React app
    print(f"Creating Vite React app: {project_name}")
    run_command(f"npm create vite@latest {project_name} -- --template react")

    # Step 2: Navigate into the project directory
    os.chdir(project_name)

    # Step 3: Install required packages
    print("Installing dependencies...")
    run_command("npm install react-icons react-redux @reduxjs/toolkit tailwindcss postcss autoprefixer react-router-dom react-spinners react-toastify axios bootstrap react-bootstrap react-router-bootstrap")
    run_command("npm install --save-dev jest @testing-library/react @testing-library/jest-dom redux-mock-store redux-thunk axios-mock-adapter babel-jest @babel/preset-env @babel/preset-react jest-fetch-mock")

    # Step 4: Initialize Tailwind CSS
    run_command("npx tailwindcss init -p")

    # Step 5: Modify tailwind.config.js
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
    with open("tailwind.config.js", "w") as tailwind_config_file:
        tailwind_config_file.write(tailwind_config_content)
    print("Updated tailwind.config.js")

    # Step 6: Modify vite.config.js
    vite_config_content = """\
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path,
      }
    }
  }
})
"""
    with open("vite.config.js", "w") as vite_config_file:
        vite_config_file.write(vite_config_content)
    print("Updated vite.config.js")

    # Step 7: Remove app.css and App.jsx
    if os.path.exists("src/App.css"):
        os.remove("src/App.css")
        print("Removed src/App.css")

    if os.path.exists("src/App.jsx"):
        os.remove("src/App.jsx")
        print("Removed src/App.jsx")

    # Step 8: Rewrite index.css
    index_css_content = """\
@tailwind base;
@tailwind components;
@tailwind utilities;
"""
    with open("src/index.css", "w") as index_css_file:
        index_css_file.write(index_css_content)
    print("Updated src/index.css")

    # Step 9: Create store.js
    store_js_content = """\
import { configureStore } from '@reduxjs/toolkit';
import { apiSlice } from './slices/apiSlice.js';

const store = configureStore({
    reducer: {
        [apiSlice.reducerPath]: apiSlice.reducer,
        
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(apiSlice.middleware),
    devTools: true,
});

export default store;
"""
    with open("src/store.js", "w") as store_file:
        store_file.write(store_js_content)
    print("Created src/store.js")

    # Step 10: Rewrite main.jsx
    main_jsx_content = """\
import { createRoot } from 'react-dom/client';
import { Provider } from 'react-redux';
import { StrictMode } from 'react';
import store from './store.js';
import {
    Route,
    createBrowserRouter,
    createRoutesFromElements,
    RouterProvider,
} from 'react-router-dom';
// import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css'
import MainLayout from './layouts/MainLayout';
import NotFoundScreen from './screens/NotFoundScreen';
import HomeScreen from './screens/HomeScreen';

function App() {
    const router = createBrowserRouter(
        createRoutesFromElements(
            <Route path='/' element={<MainLayout />}>
                <Route path='*' element={<NotFoundScreen />} />
                <Route index element={<HomeScreen />} />
            </Route>
        )
    );

    return <RouterProvider router={router} />;
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </StrictMode>
);
"""
    with open("src/main.jsx", "w") as main_file:
        main_file.write(main_jsx_content)
    print("Updated src/main.jsx")

    # Step 11: Update index.html
    index_html_content = f"""\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Ropa+Sans&display=swap" rel="stylesheet">
    <title>{project_name.replace('-', ' ')}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""
    with open("index.html", "w") as index_html_file:
        index_html_file.write(index_html_content)
    print("Updated index.html")

    # Step 12: Update README.md
    readme_content = "# Project name\n"
    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)
    print("Updated README.md to contain '# Project name'")

    # Step 13: Create screens directory and HomeScreen.jsx and NotFoundScreen.jsx
    os.makedirs("src/screens", exist_ok=True)

    home_screen_content = """\
const HomeScreen = () => {
  return (
    <>
      HomeScreen
    </>
  )
}

export default HomeScreen
"""
    with open("src/screens/HomeScreen.jsx", "w") as home_file:
        home_file.write(home_screen_content)
    print("Created src/screens/HomeScreen.jsx")

    not_found_screen_content = """\
import { Link } from 'react-router-dom'

const NotFoundScreen = () => {
    return (
        <section className='text-center flex flex-col justify-center items-center h-96'>
            <h1 className='text-6xl font-bold mb-4'>404 Not Found</h1>
            <p className='text-xl mb-5'>This page does not exist</p>
            <Link
                to='/'
                className='text-white bg-orange-400 hover:bg-orange-500 rounded-full px-3 py-3 mt-4'
            >
                Go Back
            </Link>
        </section>
    )
}

export default NotFoundScreen
"""
    with open("src/screens/NotFoundScreen.jsx", "w") as not_found_file:
        not_found_file.write(not_found_screen_content)
    print("Created src/screens/NotFoundScreen.jsx")

    # Step 14: Create layouts directory and MainLayout.jsx
    os.makedirs("src/layouts", exist_ok=True)

    # Step 14b: Create slices folder for redux
    os.makedirs("src/slices", exist_ok=True)
    
    # Step 14c: Create apiSlice.js
    api_slice_js_content = """\
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { BASE_URL } from "../constants.js";

const baseQuery = fetchBaseQuery({ baseUrl: BASE_URL });

export const apiSlice = createApi({
  baseQuery,
  tagTypes: ['User'],
  endpoints: (builder) => ({}),
});
"""
    with open("src/slices/apiSlice.js", "w") as store_file:
        store_file.write(api_slice_js_content)
    print("Created src/slices/api_slice_js_content.js")
    
    # Step 14d: Create constants.js
    constants_js_content = """\
export const BASE_URL = process.env.NODE_ENV === 'development' ? 'http://localhost:5000' : '';
export const USERS_URL = '/api/users';
"""
    with open("src/constants.js", "w") as store_file:
        store_file.write(constants_js_content)
    print("Created src/constants_js_content.js")

    main_layout_content = """\
import React from 'react'
import Header from '../components/Header'
import { Outlet } from 'react-router-dom';
import Footer from '../components/Footer';

const MainLayout = () => {
  return (
    <>
      <Header />
      <Outlet />
      <Footer />
    </>
  );
};
export default MainLayout;
"""
    with open("src/layouts/MainLayout.jsx", "w") as main_layout_file:
        main_layout_file.write(main_layout_content)
    print("Created src/layouts/MainLayout.jsx")

    # Step 15: Create components directory and Header and Footer components
    os.makedirs("src/components", exist_ok=True)

    header_content = """\
function Header() {
  return (
    <nav>
      header
    </nav>
  );
}

export default Header;
"""
    with open("src/components/Header.jsx", "w") as header_file:
        header_file.write(header_content)
    print("Created src/components/Header.jsx")

    footer_content = """\
function Footer() {
  return (
    <footer>
      footer
    </footer>
  );
}

export default Footer;
"""
    with open("src/components/Footer.jsx", "w") as footer_file:
        footer_file.write(footer_content)
    print("Created src/components/Footer.jsx")

    # Step 16: Delete react.svg from src/assets
    react_svg_path = "src/assets/react.svg"
    if os.path.exists(react_svg_path):
        os.remove(react_svg_path)
        print("Removed src/assets/react.svg")

    # Step 17: Create .babelrc
    store_js_content = """\
{
  "presets": [
    "@babel/preset-env",
    "@babel/preset-react"
  ]
}
"""
    with open("src/.babelrc", "w") as store_file:
        store_file.write(store_js_content)
    print("Created src/.babelrc")

    # Step 18: Add test script to package.json
    with open("package.json", "r") as package_file:
        package_json = json.load(package_file)

    package_json['scripts']['test'] = 'jest'

    with open("package.json", "w") as package_file:
        json.dump(package_json, package_file, indent=2)
    print("Updated package.json to include the test script.")

    print("React app setup complete!")
    webbrowser.open("http://localhost:3000/")
