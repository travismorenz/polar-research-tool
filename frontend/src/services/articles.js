export const getArticles = (_, projectId, tab = "feed", page = 0) => {
  // The controller and signal are used to make this request cancellable
  const controller = new AbortController();
  const signal = controller.signal;
  const request = fetch(
    `/api/articles/${
      projectId === "_default" ? "" : projectId
    }?tab=${tab}&page=${page}`,
    {
      method: "get",
      signal,
    }
  ).then((res) => res.json());
  // React query will use this function to abort the query
  request.cancel = () => controller.abort();
  return request;
};

export const changeArticleTab = ({ projectId, targetTab, article }) =>
  fetch(`/api/change-article-tab/${projectId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ articleId: article.id, targetTab }),
  });
