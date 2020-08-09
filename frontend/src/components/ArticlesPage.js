import React, { useState, useContext, useEffect } from "react";

import { AppContext } from "./App";
import getArticles from "../services/getArticles";

// TODO: library/register/account

const ArticlesPage = () => {
  const [page, setPage] = useState(0);
  const {
    state: { selectedProject, projects },
    action,
  } = useContext(AppContext);
  const displayArticles = projects[selectedProject].pages[page] || [];

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
      {displayArticles.length ? (
        displayArticles.map((article) => (
          <div className="article card" key={article.id}>
            <a href={article.url} target="_blank" rel="noopener noreferrer">
              <h5>{article.title}</h5>
            </a>
            <div id="authors">
              {article.authors.map((name, i) => (
                <span key={`${article.id}-${i}`}>
                  <button className="btn-link">{name}</button>
                  {i < article.authors.length - 1 ? ", " : ""}
                </span>
              ))}
            </div>
            <div className="metadata">
              <span className="publish_date">
                {article["publish_date"].slice(0, 16)}
              </span>
              {article.categories.map((name, i) => (
                <span key={`${article.id}-${name}`}>
                  <button className="btn-link">{name}</button>
                  {i < article.categories.length - 1 ? " | " : ""}
                </span>
              ))}
            </div>
            <p>{article.summary}</p>
          </div>
        ))
      ) : (
        <div className="loading loading-lg"></div>
      )}
    </div>
  );
};

export default ArticlesPage;
