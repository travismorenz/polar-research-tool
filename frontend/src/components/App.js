import React, { createContext, useEffect, useCallback } from "react";
import { useImmerReducer } from "use-immer";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import ArticlesPage from "./ArticlesPage";
import LoginPage from "./LoginPage";
import Navbar from "./Navbar";
import login from "../services/login";
import { initialState, reducer } from "../store";

export const AppContext = createContext();

const App = () => {
  const [state, dispatch] = useImmerReducer(reducer, initialState);
  const action = useCallback((type, payload) => dispatch({ type, payload }), [
    dispatch,
  ]);

  // Attempts to login using an existing session cookie. No username/pass is needed.
  useEffect(() => {
    const init = async () => {
      const { data, error } = await login({ username: "", password: "" });
      if (error) return;
      action("login", data);
    };
    init();
  }, [action]);

  return (
    <div className="app">
      <AppContext.Provider value={{ state, action }}>
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