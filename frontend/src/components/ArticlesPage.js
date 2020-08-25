import React, { useState, useContext, useEffect } from "react";

import Article from "./Article";
import ArticlesControls from "./ArticlesControls";
import { AppContext } from "./App";
import { getArticlesById } from "../services/getArticles";
import toggleArticleInLibrary from "../services/toggleArticleInLibrary";

// TODO: Docker needs to npm run build
// TODO: library/account
const pageSlice = (ids, page) =>
  ids.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE);

const PAGE_SIZE = 50;

const ArticlesPage = () => {
  const [tab, setTab] = useState("articles");
  const [page, setPage] = useState(0);
  const {
    state: { selectedProjectId, projects, articles },
    action,
  } = useContext(AppContext);
  const { id: projectId, articleIds, isLoading, libraryIds } = projects[
    selectedProjectId
  ];

  let displayedArticles =
    tab === "articles"
      ? pageSlice(articleIds, page)
      : pageSlice(libraryIds, page);
  displayedArticles = displayedArticles
    .filter((id) => articles[id])
    .map((id) => articles[id]);

  // Load articles that are needed for each page
  useEffect(() => {
    const loadArticles = async () => {
      let neededIds =
        tab === "articles"
          ? pageSlice(articleIds, page)
          : pageSlice(libraryIds, page);

      neededIds = neededIds.filter((id) => !articles[id]);

      if (!neededIds.length) return;

      action("set_project_loading", { projectId, bool: true });
      const newArticles = await getArticlesById(neededIds);
      action("add_articles", newArticles);
      action("set_project_loading", { projectId, bool: false });
    };

    // TODO: this conditional results in some unnecessary calls
    if (displayedArticles.length !== PAGE_SIZE && !isLoading) {
      loadArticles();
    }
  }, [
    action,
    articles,
    page,
    tab,
    projectId,
    articleIds,
    libraryIds,
    displayedArticles.length,
    isLoading,
  ]);

  // Set the page to 0 when changing projects
  useEffect(() => {
    setPage(0);
    setTab("articles");
  }, [selectedProjectId]);

  const toggleInLibrary = async (article_id) => {
    await toggleArticleInLibrary(selectedProjectId, article_id);
    action("toggle_in_library", {
      projectId: selectedProjectId,
      articleId: article_id,
    });
  };

  return (
    <div className="container grid-lg">
      <ArticlesControls
        tab={tab}
        setTab={setTab}
        page={page}
        setPage={setPage}
        totalCount={articleIds.length}
        libraryCount={libraryIds.length}
      />
      {/* {displayedArticles.length ? ( */}
      {displayedArticles.length && !isLoading ? (
        displayedArticles.map((article) => (
          <Article
            key={article.id}
            inLibrary={libraryIds.includes(article.id)}
            toggleInLibrary={toggleInLibrary}
            onProjectPage={selectedProjectId !== "_default"}
            {...article}
          />
        ))
      ) : (
        <div className="loading loading-lg"></div>
      )}
    </div>
  );
};

export default ArticlesPage;
