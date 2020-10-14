import React, { useState, useContext, useEffect } from "react";
import {
  isCancelledError,
  usePaginatedQuery,
  useQueryCache,
} from "react-query";

import Article from "components/Article";
import ArticleControls from "components/ArticleControls";
import { AppContext } from "components/pages/App";
import { getArticles, getLibrary } from "services/articles";
import useLibraryToggle from "hooks/useLibraryToggle";

const ArticlesPage = () => {
  const {
    state: { selectedProjectId },
  } = useContext(AppContext);
  const [tab, setTab] = useState("articles");
  const [page, setPage] = useState(0);

  // Primary queries for getting feed/library contents
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

  // Query for changing which tab an article belongs under
  const cache = useQueryCache();
  const [toggleInLibrary] = useLibraryToggle(cache);

  // Set the page to 0 when changing projects
  useEffect(() => {
    setPage(0);
    setTab("articles");
  }, [selectedProjectId]);

  const isViewingProject = selectedProjectId !== "_default";

  // Loading UI
  const isLoading =
    areArticlesLoading ||
    isLibraryLoading ||
    !articlesData ||
    (isViewingProject && !libraryData);
  if (isLoading) {
    return <div className="loading loading-lg"></div>;
  }

  // Error UI
  const error = articlesError || libraryError;
  if (error && !isCancelledError(error)) {
    // Ignore any errors caused by request cancellation
    console.log(error);
    return (
      <div>There was an error retrieving the data. Check the console.</div>
    );
  }

  // Display articles based on current tab
  const count = tab === "articles" ? articlesData.count : libraryData.count;
  let articles =
    tab === "articles" ? articlesData.articles : libraryData.articles;
  articles = articles.sort(
    (a, b) => new Date(b.publish_date) - new Date(a.publish_date)
  );

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
          inLibrary={
            isViewingProject &&
            libraryData.articles.some((a) => a.id === article.id)
          }
          toggleInLibrary={() =>
            toggleInLibrary({
              projectId: selectedProjectId,
              article,
              page,
            })
          }
          onProjectPage={selectedProjectId !== "_default"}
          {...article}
        />
      ))}
    </div>
  );
};

export default ArticlesPage;
