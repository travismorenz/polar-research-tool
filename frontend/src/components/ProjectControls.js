import React, { useEffect, useState } from "react";

import { getAllProjectNames } from "../services/projects";

const ProjectControls = ({ projects, isAdmin }) => {
  const [allProjects, setAllProjects] = useState([]);
  const [selection, setSelection] = useState(0);
  useEffect(() => {
    const init = async () => {
      const res = await getAllProjectNames();
      setAllProjects(res.projectNames);
    };
    init();
  }, []);

  const options = allProjects.filter((name) =>
    Object.values(projects).every((p) => p.name !== name)
  );

  return (
    <div className="form-group project-controls">
      <h5>Join Project</h5>
      <label className="form-inline">
        <select
          className="form-select"
          id="project-select"
          value={selection}
          onChange={(e) => setSelection(e.target.value)}
        >
          {options.map((name, i) => (
            <option value={i} key={i}>
              {name}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
};

export default ProjectControls;
