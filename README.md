# Medical Research Relevancy Tool

A tool that uses AI to suggest a relevant set of medical papers to a user based on their data (medical history, physical characteristics, demographics, etc.) without sending user data to a model. 

## Motivation, Purpose, & Goals

Cutting-edge medical research can have an incredibly positive impact on patient care & healthcare outcomes. However, on the other side of that coin, many research papers have a narrow scope and are not applicable to all patients but still greatly influence patient behavior, possibly causing unintended consequences. As such, this tool only provides users with relevant papers to prevent unsubstantiated research from influencing patient behavior.

## Points of Improvement
1. Implement stricter validation on AI's output (match to pydantic model), add assertions, conduct evals, and add retries to the AI client.
2. Widen capabilities of matching engine to convey more semantic information in the conditions, allowing for more nuanced matching.
3. Implement pre-filtering when matching users by checking that there exists some overlap between the user's profile and the paper's conditions (i.e. never run the matching algorithm if it is impossible for the match to happen).

## Design

### Key Considerations

- **Privacy**: No user data leaves the system—the matching engine runs locally using inputs from the AI and user data, which never touches the model.
- **Cost**: Each uploaded paper makes 3 API calls to OpenAI, which can then be tested against any number of user profiles.
- **Data Storage**: MongoDB's flexible schema and document-oriented storage allow for easy adaptation to changing data requirements and efficient management of complex, nested user profile data.

### Technologies

#### <u>Frontend</u>
- React 18
- Material-UI (MUI)
- React Router
- Axios

#### <u>Backend</u>
- Python 3.8+
- FastAPI
- Motor (MongoDB driver)
- OpenAI API
- PyPDF2

#### <u>Database</u>
- MongoDB

## Usage

### Prerequisites

Before you begin, ensure you have the following installed:
- Node.js (v14 or higher)
- Python 3.8 or higher
- MongoDB
- pip
- npm

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/medical-research-relevancy-tool.git
   cd medical-research-relevancy-tool
   ```

2. **Set up the Backend**

   - Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

   - Set up environment variables:
     - Create a `.env` file in the `src` directory and add your environment variables, namely `OPENAI_API_KEY` and `MONGODB_URL`.

3. **Set up the Frontend**

   - Navigate to the frontend directory:
     ```bash
     cd frontend
     ```

   - Install the required Node packages:
     ```bash
     npm install
     ```

### Running the Application

1. **Start MongoDB**
   - Ensure MongoDB is running on your system.

2. **Start the Backend Server**

   From the root directory:
   ```bash
   uvicorn src.api.app:app --reload
   ```

   The API will be available at `http://localhost:8000`.

3. **Start the Frontend Development Server**

   In a new terminal, from the frontend directory:
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`.

### Additional Information
The <i>sample_papers</i> directory contains a set of papers that may be used to test the tool.
