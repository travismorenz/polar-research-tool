import React, { useState, useContext, useEffect } from "react";

import Article from "./Article";
import ArticlesControls from "./ArticlesControls";
import { AppContext } from "./App";
import getArticles from "../services/getArticles";

// TODO: library/register/account

const ArticlesPage = () => {
  const [page, setPage] = useState(0);
  const {
    state: { selectedProjectId, projects, articles },
    action,
  } = useContext(AppContext);
  const selectedProject = projects[selectedProjectId];
  const projectPage = selectedProject.pages[page];

  useEffect(() => {
    const loadArticles = async () => {
      const { articles, count } = await getArticles(selectedProjectId, page);
      if (count) action("set_count", count);
      action("add_articles", { page, articles });
    };
    if (projects[selectedProjectId].pages[page]) return;
    loadArticles();
  }, [action, page, projects, selectedProjectId]);

  return (
    <div className="container grid-lg">
      <ArticlesControls
        activeTab="articles"
        page={page}
        setPage={setPage}
        count={selectedProject.count}
      />
      {projectPage ? (
        projectPage.map((id) => <Article key={id} {...articles[id]} />)
      ) : (
        <div className="loading loading-lg"></div>
      )}
    </div>
  );
};

export default ArticlesPage;
