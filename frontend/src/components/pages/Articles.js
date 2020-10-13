import React, { useState, useContext, useEffect } from "react";
import { usePaginatedQuery, useMutation } from "react-query";

import Article from "components/Article";
import ArticleControls from "components/ArticleControls";
import { AppContext } from "components/pages/App";
import { getArticles, getLibrary } from "services/getArticles";
import toggleArticleInLibrary from "services/toggleArticleInLibrary";

const ArticlesPage = () => {
  const {
    state: { selectedProjectId, projects },
    action,
  } = useContext(AppContext);
  const [tab, setTab] = useState("articles");
  const [page, setPage] = useState(0);

  const {
    latestData: articlesData,
    isLoading: areArticlesLoading,
    error: articlesError,
  } = usePaginatedQuery(["articles", selectedProjectId, page], getArticles);
  const {
    latestData: libraryData,
    isLoading: isLibraryLoading,
    error: libraryError,
  } = usePaginatedQuery(["library", selectedProjectId, page], getLibrary);

  // Set the page to 0 when changing projects
  useEffect(() => {
    setPage(0);
    setTab("articles");
  }, [selectedProjectId]);

  const isViewingProject = selectedProjectId !== "_default";

  const isLoading =
    areArticlesLoading ||
    isLibraryLoading ||
    !articlesData ||
    (isViewingProject && !libraryData);
  if (isLoading) {
    return <div className="loading loading-lg"></div>;
  }

  const error = articlesError || libraryError;
  if (error) {
    console.log(error);
    return (
      <div>There was an error retrieving the data. Check the console.</div>
    );
  }

  /* TODO:
    finish library adding/removing
    delete extra services
    delete extra endpoints
    delete extra reducer logic
  */
  const articles =
    tab === "articles"
      ? Object.values(articlesData.articles)
      : Object.values(libraryData.articles);
  const count = tab === "articles" ? articlesData.count : libraryData.count;
  return (
    <div className="container grid-lg">
      <ArticleControls
        count={count}
        tab={tab}
        setTab={setTab}
        page={page}
        setPage={setPage}
        showLibrary={isViewingProject}
      />
      {articles.map((article) => (
        <Article
          key={article.id}
          inLibrary={isViewingProject && !!libraryData.articles[article.id]}
          // toggleInLibrary={toggleInLibrary}
          onProjectPage={selectedProjectId !== "_default"}
          {...article}
        />
      ))}
    </div>
  );
};

export default ArticlesPage;
