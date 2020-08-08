import React, { useState, createContext, useEffect } from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import LoginPage from "./LoginPage";
import Navbar from "./Navbar";
import login from "../services/login";

export const AppContext = createContext();

const Main = () => <div>Main</div>;

const App = () => {
  const [state, setState] = useState({
    username: "",
    isLoggedIn: false,
    projects: [],
    selectedProject: "",
  });

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
            <Route exact path="/" component={Main} />
            <Route exact path="/login" component={LoginPage} />
            <Redirect to="/" />
          </Switch>
        </BrowserRouter>
      </AppContext.Provider>
    </div>
  );
};

export default App;
