import httpx
from typing import List, Dict, Optional
from app.core.config import settings

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def get_repository(self, owner: str, repo: str) -> Optional[Dict]:
        """Get repository information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return None
    
    async def get_pull_request(self, owner: str, repo: str, pr_number: int) -> Optional[Dict]:
        """Get pull request details"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return None
    
    async def get_pull_request_files(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        """Get files changed in a pull request"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return []
    
    async def get_file_content(self, owner: str, repo: str, path: str, ref: str = "main") -> Optional[str]:
        """Get file content from repository"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/contents/{path}",
                headers=self.headers,
                params={"ref": ref}
            )
            if response.status_code == 200:
                import base64
                content = response.json()["content"]
                return base64.b64decode(content).decode("utf-8")
            return None
    
    async def get_pull_request_diff(self, owner: str, repo: str, pr_number: int) -> str:
        """Get unified diff for pull request"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}",
                headers=self.headers,
                params={"mediaType": "application/vnd.github.v3.diff"}
            )
            if response.status_code == 200:
                return response.text
            return ""
    
    async def create_review_comment(self, owner: str, repo: str, pr_number: int, 
                                  commit_id: str, path: str, position: int, 
                                  body: str) -> Optional[Dict]:
        """Create a review comment on a pull request"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/comments",
                headers=self.headers,
                json={
                    "commit_id": commit_id,
                    "path": path,
                    "position": position,
                    "body": body
                }
            )
            if response.status_code == 201:
                return response.json()
            return None
    
    async def get_user_repositories(self, username: str) -> List[Dict]:
        """Get repositories for a user"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/users/{username}/repos",
                headers=self.headers,
                params={"sort": "updated", "per_page": 100}
            )
            if response.status_code == 200:
                return response.json()
            return []
    
    async def get_repository_pull_requests(self, owner: str, repo: str, 
                                         state: str = "open") -> List[Dict]:
        """Get pull requests for a repository"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/pulls",
                headers=self.headers,
                params={"state": state, "per_page": 100}
            )
            if response.status_code == 200:
                return response.json()
            return []
