import React, { createContext, useEffect, useCallback } from "react";
import { ReactQueryCacheProvider, QueryCache } from "react-query";
import { useImmerReducer } from "use-immer";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import Account from "components/pages/Account";
import Articles from "components/pages/Articles";
import Login from "components/pages/Login";
import Register from "components/pages/Register";
import Navbar from "components/Navbar";
import { login } from "services/auth";
import { initialState, reducer } from "store";

export const AppContext = createContext();
export const queryCache = new QueryCache();

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
        <ReactQueryCacheProvider queryCache={queryCache}>
          <BrowserRouter>
            <Navbar />
            <Switch>
              <Route exact path="/" component={Articles} />
              <Route exact path="/login" component={Login} />
              <Route exact path="/register" component={Register} />
              <Route exact path="/account" component={Account} />
              <Redirect to="/" />
            </Switch>
          </BrowserRouter>
        </ReactQueryCacheProvider>
      </AppContext.Provider>
    </div>
  );
};

export default App;
