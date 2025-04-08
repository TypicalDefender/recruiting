-- Resume table to store basic information
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    location VARCHAR(255),
    years_of_experience DECIMAL(4,1),  -- YOE field
    current_salary DECIMAL(12,2),      -- SALARY field
    experience_level VARCHAR(50),       -- EXPERIENCE field
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Skills table for storing available skills
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Junction table for resume-skills many-to-many relationship
CREATE TABLE resume_skills (
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    years_of_experience DECIMAL(4,1),  -- Experience with this particular skill
    PRIMARY KEY (resume_id, skill_id)
);

-- Education table for storing educational background
CREATE TABLE education (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    degree VARCHAR(100) NOT NULL,      -- e.g., "Bachelor Degree", "Master Degree"
    field_of_study VARCHAR(255),       -- e.g., "Computer Science"
    institution VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    start_date DATE,
    end_date DATE,
    gpa DECIMAL(3,2)
);

-- Work experience table
CREATE TABLE work_experience (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    start_date DATE NOT NULL,
    end_date DATE,  -- NULL if current position
    description TEXT,
    is_current BOOLEAN DEFAULT FALSE
);

-- Projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    url VARCHAR(512)  -- For project links/github etc.
);

-- Project skills junction table
CREATE TABLE project_skills (
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (project_id, skill_id)
);

-- Certifications table
CREATE TABLE certifications (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    issuing_organization VARCHAR(255) NOT NULL,
    issue_date DATE,
    expiry_date DATE,
    credential_id VARCHAR(255)
);

-- Create indexes for commonly queried fields
CREATE INDEX idx_resumes_yoe ON resumes(years_of_experience);
CREATE INDEX idx_resumes_location ON resumes(location);
CREATE INDEX idx_resumes_experience_level ON resumes(experience_level);
CREATE INDEX idx_skills_name ON skills(name);
CREATE INDEX idx_education_degree ON education(degree);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update the updated_at column
CREATE TRIGGER update_resumes_updated_at
    BEFORE UPDATE ON resumes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column(); 