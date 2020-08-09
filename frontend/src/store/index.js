const createProject = ({ name, id }) => ({ name, id, pages: [] });

export const initialState = {
  username: "",
  isLoggedIn: false,
  projects: {
    "": { name: "None", id: "", pages: [] },
  },
  selectedProject: "",
};

export const reducer = (state, action) => {
  switch (action.type) {
    case "add_articles": {
      const { page, articles } = action.payload;
      if (!state.projects[state.selectedProject].pages)
        state.project[state.selectedProject].pages = [];
      state.projects[state.selectedProject].pages[page] = articles;
      break;
    }
    case "set_count":
      state.projects[state.selectedProject].count = action.payload;
      break;
    case "select_project":
      state.selectedProject = action.payload;
      break;
    case "login":
      state.isLoggedIn = true;
      state.username = action.payload.username;
      action.payload.projects.forEach(
        (p) => (state.projects[p.id] = createProject(p))
      );
      break;
    case "logout":
      return initialState;
    default:
      return state;
  }
};
