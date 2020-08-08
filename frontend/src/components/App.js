import React, { useState, createContext, useEffect } from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import ArticlesPage from "./ArticlesPage";
import LoginPage from "./LoginPage";
import Navbar from "./Navbar";
import login from "../services/login";

export const AppContext = createContext();
export const initialState = {
  username: "",
  isLoggedIn: false,
  projects: [],
  selectedProject: "",
};

const App = () => {
  const [state, setState] = useState(initialState);

  // Attempts to login using an existing session cookie. No username/pass is needed.
  useEffect(() => {
    const init = async () => {
      const { data, error } = await login({ username: "", password: "" });
      if (error) return;
      setState((s) => ({ ...s, isLoggedIn: true, ...data }));
    };
    init();
  }, []);

  return (
    <div className="app">
      <AppContext.Provider value={{ state, setState }}>
        <BrowserRouter>
          <Navbar />
          <Switch>
            <Route exact path="/" component={ArticlesPage} />
            <Route exact path="/login" component={LoginPage} />
            <Redirect to="/" />
          </Switch>
        </BrowserRouter>
      </AppContext.Provider>
    </div>
  );
};

export default App;
