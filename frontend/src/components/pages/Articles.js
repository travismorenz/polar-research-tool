import React, { useState, useContext, useEffect } from "react";
import {
  usePaginatedQuery,
  useMutation,
  useQueryCache,
  isCancelledError,
} from "react-query";

import Article from "components/Article";
import ArticleControls from "components/ArticleControls";
import { AppContext } from "components/pages/App";
import { getArticles, getLibrary } from "services/getArticles";
import toggleArticleInLibrary from "services/toggleArticleInLibrary";

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

  // Query for optimistically updating an article's classification
  const cache = useQueryCache();
  const [toggleInLibrary] = useMutation(toggleArticleInLibrary, {
    onMutate: ({ article, projectId, page }) => {
      const queryKey = ["library", projectId, page];
      const oldLibrary = cache.getQueryData(queryKey);
      cache.cancelQueries(queryKey);
      cache.setQueryData(queryKey, (old) => {
        const isInLibrary = old.articles.includes(article);
        const articles = isInLibrary
          ? old.articles.filter((a) => a !== article)
          : [...old.articles, article];
        const count = isInLibrary ? old.count - 1 : old.count + 1;
        return { articles, count };
      });
      return oldLibrary;
    },
    onError: (data, { projectId, page }, snapShot) =>
      cache.setQueryData(["library", projectId, page], snapShot),
    onSuccess: (data, { projectId, page }) =>
      cache.invalidateQueries(["library", projectId, page]),
  });

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
