const createProject = ({ name, id }) => ({ name, id, pages: [] });

export const initialState = {
  username: "",
  isLoggedIn: false,
  projects: {
    "": { name: "None", id: "", pages: [] },
  },
  articles: {},
  selectedProjectId: "",
};

export const reducer = (state, action) => {
  switch (action.type) {
    case "add_articles": {
      const { page, articles } = action.payload;
      articles.forEach((a) => {
        // Create new page if one doesn't exist
        if (!state.projects[state.selectedProjectId].pages[page])
          state.projects[state.selectedProjectId].pages[page] = [];
        // Add article id to page if it doesn't exist
        if (!state.projects[state.selectedProjectId].pages[page].includes(a.id))
          state.projects[state.selectedProjectId].pages[page].push(a.id);
        // Add article to articles if it doesn't exist
        if (!state.articles[a.id]) state.articles[a.id] = a;
      });
      break;
    }
    case "set_count":
      state.projects[state.selectedProjectId].count = action.payload;
      break;
    case "select_project":
      state.selectedProjectId = action.payload;
      break;
    case "login":
      state.isLoggedIn = true;
      state.username = action.payload.username;
      // Fill out each pulled in project with needed fields
      action.payload.projects.forEach((p) => {
        if (!state.projects[p.id]) state.projects[p.id] = createProject(p);
      });
      break;
    case "logout":
      return { ...initialState };
    default:
      return state;
  }
};
