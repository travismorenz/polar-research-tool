import React, { useState, createContext, useEffect } from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";
import LoginPage from "./LoginPage";
import login from "../services/login";

export const AppContext = createContext();

const Main = () => <div>Main</div>;

const App = () => {
  const [state, setState] = useState({
    username: "",
    isLoggedIn: false,
  });

  // Attempts to login using an existing session cookie. No username/pass is needed.
  useEffect(() => {
    const init = async () => {
      const { data, error } = await login({ username: "", password: "" });
      if (error) return;
      setState({ isLoggedIn: true, username: data });
    };
    init();
  }, []);

  return (
    <div className="app">
      <AppContext.Provider value={{ state, setState }}>
        <BrowserRouter>
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
