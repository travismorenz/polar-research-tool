import { useMutation } from "react-query";
import { toggleInLibrary } from "services/articles";

// TODO: Modify for toggling articles between all tabs
// Hook for optimistically toggling articles in/out of a project library
export default (cache) =>
  useMutation(toggleInLibrary, {
    onMutate: ({ article, projectId, page }) => {
      // Construct the key used to identify the last library query
      const queryKey = ["library", projectId, page];

      // Create a snapshot of the library data at this time
      const oldLibrary = cache.getQueryData(queryKey);

      // Cancel any outgoing library queries
      cache.cancelQueries(queryKey);

      // Optimistically toggle the article in/out of the library and update the count
      cache.setQueryData(queryKey, (old) => {
        const isInLibrary = old.articles.includes(article);
        const articles = isInLibrary
          ? old.articles.filter((a) => a !== article)
          : [...old.articles, article];
        const count = isInLibrary ? old.count - 1 : old.count + 1;
        return { articles, count };
      });

      // Return a rollback function that will be used if the mutation request fails
      return () => cache.setQueryData(queryKey, oldLibrary);
    },
    // Use the rollback function on error
    onError: (data, variables, rollback) => () => rollback(),
    // Refetch library on success
    onSuccess: (data, { projectId, page }) =>
      cache.invalidateQueries(["library", projectId, page]),
  });
