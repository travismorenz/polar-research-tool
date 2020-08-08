import React, { useContext, useEffect } from "react";

import { AppContext } from "./App";
import getArticles from "../services/getArticles";

// TODO: proxy
// TODO: library/register/account

const ArticlesPage = () => {
  const {
    state: { selectedProject, articles },
    setState,
  } = useContext(AppContext);
  const displayArticles = articles[`${selectedProject}`] || []; //TODO: page

  useEffect(() => {
    const loadArticles = async () => {
      const newArticles = await getArticles(selectedProject); //TODO: page
      setState((s) => ({
        ...s,
        articles: { ...s.articles, [`${selectedProject}`]: newArticles }, //TODO: page
      }));
    };

    if (articles[`${selectedProject}`]) return;
    loadArticles();
  }, [articles, selectedProject, setState]);

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
