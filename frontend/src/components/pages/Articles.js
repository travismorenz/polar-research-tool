import React, { useState, useContext, useEffect } from "react";
import {
  isCancelledError,
  usePaginatedQuery,
  useQueryCache,
} from "react-query";

import Article from "components/Article";
import ArticleControls from "components/ArticleControls";
import { AppContext } from "components/pages/App";
import { getArticles } from "services/articles";
import useLibraryToggle from "hooks/useLibraryToggle";

const ArticlesPage = () => {
  const {
    state: { selectedProjectId },
  } = useContext(AppContext);
  const [tab, setTab] = useState("feed");
  const [page, setPage] = useState(0);

  // Articles query
  const { latestData, isLoading, error } = usePaginatedQuery(
    ["articles", selectedProjectId, tab, page],
    getArticles
  );

  // Query for changing which tab an article belongs under
  const cache = useQueryCache();
  const [toggleInLibrary] = useLibraryToggle(cache);

  // Reset page state on project change
  useEffect(() => {
    setPage(0);
    setTab("feed");
  }, [selectedProjectId]);

  const isViewingProject = selectedProjectId !== "_default";

  // Loading UI
  if (isLoading || !latestData) {
    return <div className="loading loading-lg"></div>;
  }

  // Error UI
  if (error && !isCancelledError(error)) {
    // Ignore any errors caused by request cancellation
    console.log(error);
    return (
      <div>There was an error retrieving the data. Check the console.</div>
    );
  }

  // Display articles based on current tab
  const count = latestData.count;
  let articles = latestData.articles.sort(
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
          toggleInLibrary={() =>
            toggleInLibrary({
              projectId: selectedProjectId,
              article,
              tab,
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
