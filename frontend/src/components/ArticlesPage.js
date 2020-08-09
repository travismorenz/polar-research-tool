import React, { useState, useContext, useEffect } from "react";

import Article from "./Article";
import { AppContext } from "./App";
import getArticles from "../services/getArticles";

// TODO: library/register/account

const ArticlesPage = () => {
  const [page, setPage] = useState(0);
  const {
    state: { selectedProject, projects, articles },
    action,
  } = useContext(AppContext);
  const projectPage = projects[selectedProject].pages[page];

  useEffect(() => {
    const loadArticles = async () => {
      const { articles, count } = await getArticles(selectedProject);
      if (count) action("set_count", count);
      action("add_articles", { page, articles });
    };
    if (projects[selectedProject].pages[page]) return;
    loadArticles();
  }, [action, page, projects, selectedProject]);

  return (
    <div className="container grid-lg">
      <div className="space-between">
        <div className="tabs">
          <div className="btn-group btn-group-block" id="pagebar"></div>
        </div>
        <form id="search-bar" className="has-icon-left"></form>
      </div>
      {projectPage ? (
        projectPage.map((id) => <Article key={id} {...articles[id]} />)
      ) : (
        <div className="loading loading-lg"></div>
      )}
    </div>
  );
};

export default ArticlesPage;
