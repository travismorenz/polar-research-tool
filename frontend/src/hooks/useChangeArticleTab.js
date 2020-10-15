import { useMutation } from "react-query";
import { changeArticleTab } from "services/articles";

// Hook for optimistically switching articles between tabs
export default (cache) =>
  useMutation(changeArticleTab, {
    onMutate: ({ article, projectId, tab, page }) => {
      // Construct the key used to identify the last library query
      const queryKey = ["articles", projectId, tab, page];

      // Create a snapshot of the library data at this time
      const oldLibrary = cache.getQueryData(queryKey);

      // Cancel any outgoing library queries
      cache.cancelQueries(queryKey);

      // Optimistically toggle the article in/out of the library and update the count
      cache.setQueryData(queryKey, (old) => {
        const articles = old.articles.filter((a) => a !== article);
        const count = old.count - 1;
        return { articles, count };
      });

      // Return a rollback function that will be used if the mutation request fails
      return () => cache.setQueryData(queryKey, oldLibrary);
    },
    // Use the rollback function on error
    onError: (_, __, rollback) => () => rollback(),
    // Refetch library on success
    onSuccess: (_, { projectId, tab, page }) =>
      cache.invalidateQueries(["articles", projectId, tab, page]),
  });
