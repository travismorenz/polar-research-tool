import React, { createContext, useEffect, useCallback } from "react";
import { useImmerReducer } from "use-immer";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import Account from "components/pages/Account";
import Articles from "components/pages/Articles";
import Login from "components/pages/Login";
import Register from "components/pages/Register";
import Navbar from "components/Navbar";
import { login } from "services/auth";
import { initialState, reducer } from "store";
import { getArticleIds, getLibraryIds } from "services/getArticles";

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

  // Load the article ids for each project
  useEffect(() => {
    const loadArticleIds = async (projectId) => {
      action("set_project_loading", { projectId, bool: true });
      const { ids: articleIds } = await getArticleIds(projectId);

      let libraryIds = [];
      if (projectId !== "_default") {
        const { ids } = await getLibraryIds(projectId);
        libraryIds = ids;
      }

      action("set_article_ids", { projectId, articleIds });
      action("set_library_ids", { projectId, libraryIds });
      action("set_project_loading", { projectId, bool: false });
    };

    for (let project of Object.values(state.projects)) {
      if (!project.isLoading && !project.articleIds.length)
        loadArticleIds(project.id);
    }
  }, [state.projects, action]);

  return (
    <div className="app">
      <AppContext.Provider value={{ state, action }}>
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
      </AppContext.Provider>
    </div>
  );
};

export default App;