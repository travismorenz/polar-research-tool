import React, { useState, useContext, useEffect } from "react";

import Article from "./Article";
import ArticlesControls from "./ArticlesControls";
import { AppContext } from "./App";
import { getArticlesById } from "../services/getArticles";

// TODO: library/register/account
const pageSlice = (ids, page) =>
  ids.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE);

const PAGE_SIZE = 50;

const ArticlesPage = () => {
  const [page, setPage] = useState(0);
  const {
    state: { selectedProjectId, projects, articles },
    action,
  } = useContext(AppContext);
  const { articleIds, isLoading, libraryIds } = projects[selectedProjectId];
  const displayedArticles = pageSlice(articleIds, page)
    .filter((id) => articles[id])
    .map((id) => articles[id]);

  // Load articles that are needed for each page
  useEffect(() => {
    const loadArticles = async () => {
      const neededIds = pageSlice(articleIds, page).filter(
        (id) => !articles[id]
      );

      if (!neededIds.length) return;

      action("set_project_loading", { projectId: id, bool: true });
      const newArticles = await getArticlesById(neededIds);
      action("add_articles", newArticles);
      action("set_project_loading", { projectId: id, bool: false });
    };

    const { id, articleIds, isLoading } = projects[selectedProjectId];
    if (displayedArticles.length !== PAGE_SIZE && !isLoading) {
      loadArticles();
    }
  }, [
    action,
    articles,
    page,
    projects,
    selectedProjectId,
    displayedArticles.length,
  ]);

  // Set the page to 0 when changing projects
  useEffect(() => setPage(0), [selectedProjectId]);

  return (
    <div className="container grid-lg">
      <ArticlesControls
        activeTab="articles"
        page={page}
        setPage={setPage}
        count={articleIds.length}
        showLibrary={!!libraryIds.length}
      />
      {/* {displayedArticles.length ? ( */}
      {displayedArticles.length && !isLoading ? (
        displayedArticles.map((article) => (
          <Article key={article.id} {...article} />
        ))
      ) : (
        <div className="loading loading-lg"></div>
      )}
    </div>
  );
};

export default ArticlesPage;
