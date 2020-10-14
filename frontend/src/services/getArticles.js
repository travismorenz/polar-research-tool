export const getArticles = (_, projectId, page = 0) => {
  // The controller and signal are used to make this request cancellable
  const controller = new AbortController();
  const signal = controller.signal;
  const request = fetch(
    `/api/articles/${projectId === "_default" ? "" : projectId}?page=${page}`,
    {
      method: "get",
      signal,
    }
  ).then((res) => res.json());
  // React query will use this function to abort the query
  request.cancel = () => controller.abort();
  return request;
};

export const getLibrary = (_, projectId, page = 0) => {
  if (projectId === "_default") return;

  // The controller and signal are used to make this request cancellable
  const controller = new AbortController();
  const signal = controller.signal;
  const request = fetch(`/api/articles/library/${projectId}?page=${page}`, {
    method: "get",
    signal,
  }).then((res) => res.json());
  // React query will use this function to abort the query
  request.cancel = () => controller.abort();

  return request;
};
