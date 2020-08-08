import React, { useContext, useEffect } from "react";

import { AppContext } from "./App";
import getArticles from "../services/getArticles";

const ArticlesPage = () => {
  const {
    state: { selectedProject, articles },
    setState,
  } = useContext(AppContext);
  const displayArticles = articles[`${selectedProject}`]; //TODO: page

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
      {displayArticles && displayArticles.map((x) => <div>{x.title}</div>)}
    </div>
  );
};

export default ArticlesPage;
