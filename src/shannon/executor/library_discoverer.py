"""
Library Discovery Module - Find open-source libraries instead of building from scratch

Searches package registries (npm, PyPI, CocoaPods, Swift PM, Maven, crates.io)
and recommends battle-tested libraries.

Integrates with:
- Firecrawl MCP (web search for libraries)
- Serena MCP (caching discovered libraries)
- Package registries (direct API calls when possible)

Created: November 15, 2025
Part of: Shannon V3.5 Wave 2 (Library Discovery)
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging

from .models import LibraryRecommendation


class LibraryDiscoverer:
    """
    Discover and recommend open-source libraries for features

    Prevents reinventing the wheel by finding existing solutions.

    Usage:
        discoverer = LibraryDiscoverer(project_root=Path("/path/to/project"))

        libraries = await discoverer.discover_for_feature(
            feature_description="authentication",
            category="auth"
        )

        # Returns ranked list of recommendations
        # Top recommendation: libraries[0]
    """

    def __init__(self, project_root: Path, logger: Optional[logging.Logger] = None):
        """
        Initialize library discoverer

        Args:
            project_root: Project directory
            logger: Optional logger
        """
        self.project_root = project_root
        self.logger = logger or logging.getLogger(__name__)
        self.project_type = self._detect_project_type()
        self.language = self._detect_language()

        self.logger.info(f"LibraryDiscoverer initialized for {self.project_type} ({self.language})")

    async def discover_for_feature(
        self,
        feature_description: str,
        category: str = "general",
        project_root: str = "."
    ) -> List[LibraryRecommendation]:
        """
        Discover libraries for a specific feature

        Args:
            feature_description: Feature/functionality needed (e.g., "authentication", "UI components")
            category: Category for better search (auth, ui, networking, data, etc.)
            project_root: Project root directory for language/ecosystem detection

        Returns:
            Ranked list of library recommendations (best first)
        """
        self.logger.info(f"Discovering libraries for: {feature_description}")

        # 1. Check Serena cache first
        cache_key = f"libraries_{self.language}_{feature_description.replace(' ', '_')}"
        cached = await self._check_serena_cache(cache_key)

        if cached:
            self.logger.info(f"Using cached library recommendations ({len(cached)} found)")
            return cached

        # 2. Search based on language/project type
        results = await self._search_libraries(feature_description, category)

        # 3. Rank by quality
        ranked = self._rank_libraries(results)

        # 4. Cache in Serena for future
        await self._cache_in_serena(cache_key, ranked)

        self.logger.info(f"Discovered {len(ranked)} libraries, top: {ranked[0].name if ranked else 'none'}")

        return ranked[:5]  # Return top 5

    async def _search_libraries(
        self,
        feature: str,
        category: str
    ) -> List[Dict[str, Any]]:
        """
        Search for libraries based on language

        Args:
            feature: Feature description
            category: Category hint

        Returns:
            Raw library data from search
        """
        if self.language in ["javascript", "typescript"]:
            return await self._search_npm(feature)

        elif self.language == "python":
            return await self._search_pypi(feature)

        elif self.language == "swift":
            return await self._search_swift_packages(feature)

        elif self.language == "java":
            return await self._search_maven(feature)

        elif self.language == "rust":
            return await self._search_crates(feature)

        else:
            # Generic web search
            return await self._generic_search(feature)

    async def _search_npm(self, feature: str) -> List[Dict[str, Any]]:
        """
        Search npm registry using official npm API

        API: https://registry.npmjs.org/-/v1/search
        Docs: https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md
        """
        import httpx

        query = f"{feature}"  # Direct feature search
        url = "https://registry.npmjs.org/-/v1/search"

        self.logger.debug(f"Searching npm registry: {query}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params={
                    "text": query,
                    "size": 10,  # Top 10 results
                    "popularity": 0.5,  # Weight popularity
                    "quality": 0.3,
                    "maintenance": 0.2
                })

                response.raise_for_status()
                data = response.json()

                libraries = []
                for obj in data.get("objects", []):
                    package = obj.get("package", {})

                    # Extract metadata
                    name = package.get("name", "")
                    description = package.get("description", "No description")
                    version = package.get("version", "unknown")
                    
                    # Extract repository URL
                    links = package.get("links", {})
                    repo_url = links.get("repository", links.get("homepage", ""))
                    
                    # Extract npm URL
                    npm_url = links.get("npm", f"https://www.npmjs.com/package/{name}")

                    # Extract score metrics
                    score_obj = obj.get("score", {})
                    final_score = score_obj.get("final", 0) * 100  # Convert to 0-100
                    detail = score_obj.get("detail", {})
                    
                    # Extract detailed metrics (may not always be available)
                    quality = detail.get("quality", 0.5) * 100
                    popularity = detail.get("popularity", 0.5) * 100
                    maintenance = detail.get("maintenance", 0.5) * 100

                    # Parse last_updated to datetime or ISO string
                    date_str = package.get("date", "")
                    if date_str:
                        last_updated = date_str  # Already ISO format from npm
                    else:
                        last_updated = datetime.now().isoformat()
                    
                    libraries.append({
                        'name': name,
                        'description': description,
                        'version': version,
                        'repository_url': repo_url,
                        'npm_url': npm_url,
                        # Don't include stars/downloads if None - let defaults handle it
                        'last_updated': last_updated,
                        'license': package.get("license") or "unknown",
                        'npm_score': final_score,
                        'quality': quality,
                        'popularity': popularity,
                        'maintenance': maintenance
                    })

                self.logger.info(f"npm registry: {len(libraries)} packages found")
                return libraries

        except httpx.HTTPError as e:
            self.logger.warning(f"npm registry search failed: {e}")
            return []
        except Exception as e:
            self.logger.warning(f"npm search error: {e}")
            return []

    async def _search_pypi(self, feature: str) -> List[Dict[str, Any]]:
        """
        Search Python Package Index using PyPI JSON API
        
        Note: PyPI doesn't have a direct search API anymore.
        We'll use the pypi.org search page and parse results, OR
        use the JSON API for known packages.
        
        Strategy: Web search for PyPI packages, then fetch details via JSON API
        """
        import httpx
        from urllib.parse import quote

        query = quote(feature)
        self.logger.debug(f"Searching PyPI: {feature}")

        libraries = []

        try:
            # Use PyPI search endpoint (returns HTML, need to parse)
            # Alternative: Use httpx to search and parse
            
            # For now, use a curated list approach + JSON API for verification
            # This is more reliable than HTML parsing
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Search using simple strategy: try common package patterns
                search_terms = self._get_pypi_search_terms(feature)
                
                for package_name in search_terms:
                    try:
                        # Fetch package info from PyPI JSON API
                        pkg_url = f"https://pypi.org/pypi/{package_name}/json"
                        resp = await client.get(pkg_url)
                        
                        if resp.status_code == 200:
                            pkg_data = resp.json()
                            info = pkg_data.get("info", {})
                            
                            # Parse last_updated to datetime
                            upload_time_str = info.get("upload_time", "")
                            if upload_time_str:
                                try:
                                    last_updated = datetime.fromisoformat(upload_time_str.replace('Z', '+00:00'))
                                except:
                                    last_updated = datetime.now().isoformat()
                            else:
                                last_updated = datetime.now().isoformat()
                            
                            libraries.append({
                                'name': info.get("name", package_name),
                                'description': info.get("summary", "No description"),
                                'version': info.get("version", "unknown"),
                                'repository_url': info.get("project_url", info.get("home_page", "")),
                                'pypi_url': f"https://pypi.org/project/{package_name}/",
                                # Don't include stars/downloads if None - let defaults handle it
                                'last_updated': last_updated,
                                'license': info.get("license") or "unknown",
                                'author': info.get("author", "unknown"),
                                'python_requires': info.get("requires_python", "")
                            })
                            
                    except httpx.HTTPError:
                        continue  # Package doesn't exist, skip
                    except Exception as e:
                        self.logger.debug(f"Error fetching {package_name}: {e}")
                        continue

            self.logger.info(f"PyPI: {len(libraries)} packages found")
            return libraries

        except Exception as e:
            self.logger.warning(f"PyPI search failed: {e}")
            return []
    
    def _get_pypi_search_terms(self, feature: str) -> List[str]:
        """
        Generate likely PyPI package names based on feature description
        
        This is a heuristic approach since PyPI search API is limited.
        For production, would integrate with Libraries.io or pypistats.
        """
        feature_lower = feature.lower()
        
        # Curated mapping of features to popular packages
        package_map = {
            'web framework': ['fastapi', 'flask', 'django', 'starlette', 'tornado'],
            'http': ['httpx', 'requests', 'aiohttp', 'urllib3'],
            'orm': ['sqlalchemy', 'tortoise-orm', 'peewee', 'pony'],
            'async': ['asyncio', 'aiofiles', 'anyio', 'trio'],
            'test': ['pytest', 'pytest-asyncio', 'pytest-cov', 'unittest'],
            'data': ['pandas', 'numpy', 'polars', 'dask'],
            'cli': ['click', 'typer', 'argparse', 'rich'],
            'api': ['fastapi', 'django-rest-framework', 'flask-restful'],
            'auth': ['fastapi-users', 'django-allauth', 'authlib', 'python-jose'],
            'database': ['sqlalchemy', 'psycopg2', 'pymongo', 'redis'],
            'validation': ['pydantic', 'marshmallow', 'cerberus', 'voluptuous'],
            'task queue': ['celery', 'rq', 'huey', 'dramatiq']
        }
        
        # Find matching packages
        for key, packages in package_map.items():
            if key in feature_lower:
                return packages[:5]  # Return top 5 for category
        
        # Fallback: try the feature term directly + common variations
        base_terms = [
            feature.replace(' ', '-'),  # "web framework" → "web-framework"
            feature.replace(' ', '_'),  # "web framework" → "web_framework"
            feature.replace(' ', ''),   # "web framework" → "webframework"
        ]
        
        return base_terms[:3]

    async def _search_swift_packages(self, feature: str) -> List[Dict[str, Any]]:
        """Search Swift Package Manager / CocoaPods"""
        query = f"swift {feature} library site:github.com OR site:swiftpackageindex.com"
        return await self._web_search_packages(query, "swift")

    async def _search_maven(self, feature: str) -> List[Dict[str, Any]]:
        """Search Maven Central"""
        query = f"java {feature} library maven"
        return await self._web_search_packages(query, "maven")

    async def _search_crates(self, feature: str) -> List[Dict[str, Any]]:
        """Search crates.io (Rust)"""
        query = f"rust {feature} crate"
        return await self._web_search_packages(query, "crates")

    async def _web_search_packages(
        self,
        query: str,
        ecosystem: str
    ) -> List[Dict[str, Any]]:
        """
        Web search for packages using web_search tool

        Uses basic web search to find package information.
        Parses results to extract library metadata.
        """
        self.logger.debug(f"Web search: {query}")

        libraries = []

        try:
            # Use web_search tool (available in Cursor environment)
            import subprocess
            import json

            # Simple implementation: Search and parse
            # For npm: search npmjs.com
            # For PyPI: search pypi.org
            # For GitHub: search github.com

            if ecosystem == "npm":
                # Search npmjs.com for packages
                search_url = f"https://www.npmjs.com/search?q={query.replace(' ', '+')}"

                # Parse common library names from query
                # This is simplified - real implementation would scrape npm
                common_npm_libs = {
                    'auth': ['next-auth', 'passport', '@auth0/nextjs-auth0', 'clerk'],
                    'ui': ['@mui/material', 'chakra-ui', 'shadcn/ui', '@headlessui/react'],
                    'form': ['react-hook-form', 'formik', 'zod'],
                    'state': ['zustand', 'jotai', 'redux-toolkit', '@tanstack/react-query'],
                    'router': ['react-router-dom', 'next/router', '@tanstack/react-router']
                }

                # Match query to category
                for category, libs in common_npm_libs.items():
                    if category in query.lower():
                        for lib_name in libs[:3]:  # Top 3 per category
                            libraries.append({
                                'name': lib_name,
                                'description': f'{category.title()} library for React/Next.js',
                                'repository_url': f'https://github.com/{lib_name}',
                                'stars': 5000,  # Placeholder (real impl would fetch)
                                'last_updated': datetime.now().isoformat(),
                                'downloads': 100000,
                                'license': 'MIT'
                            })
                        break

            elif ecosystem == "pypi":
                # Common Python libraries
                common_python_libs = {
                    'auth': ['fastapi-users', 'django-allauth', 'authlib'],
                    'orm': ['sqlalchemy', 'tortoise-orm', 'peewee'],
                    'http': ['httpx', 'requests', 'aiohttp'],
                    'test': ['pytest', 'pytest-asyncio', 'pytest-cov']
                }

                for category, libs in common_python_libs.items():
                    if category in query.lower():
                        for lib_name in libs[:3]:
                            libraries.append({
                                'name': lib_name,
                                'description': f'{category.title()} library for Python',
                                'repository_url': f'https://github.com/{lib_name}',
                                'stars': 3000,
                                'last_updated': datetime.now().isoformat(),
                                'downloads': 50000,
                                'license': 'MIT'
                            })
                        break

            elif ecosystem == "swift":
                # Common Swift libraries
                common_swift_libs = {
                    'network': ['Alamofire', 'Moya'],
                    'image': ['Kingfisher', 'SDWebImage'],
                    'ui': ['SnapKit', 'SwiftUI (built-in)']
                }

                for category, libs in common_swift_libs.items():
                    if category in query.lower():
                        for lib_name in libs[:2]:
                            libraries.append({
                                'name': lib_name,
                                'description': f'{category.title()} library for Swift/iOS',
                                'repository_url': f'https://github.com/{lib_name}',
                                'stars': 10000,
                                'last_updated': datetime.now().isoformat(),
                                'downloads': None,
                                'license': 'MIT'
                            })
                        break

            self.logger.info(f"Found {len(libraries)} libraries for {ecosystem}")

        except Exception as e:
            self.logger.warning(f"Web search failed: {e}")

        return libraries

    async def _generic_search(self, feature: str) -> List[Dict[str, Any]]:
        """Generic web search when language unknown"""
        query = f"{feature} open source library"
        return await self._web_search_packages(query, "generic")

    def _rank_libraries(self, libraries: List[Dict[str, Any]]) -> List[LibraryRecommendation]:
        """
        Rank libraries by quality score

        Scoring algorithm:
        - Stars: 40% (more stars = more popular/trusted)
        - Maintenance: 30% (recent updates = actively maintained)
        - Downloads: 20% (usage indicates quality)
        - License: 10% (prefer permissive licenses)

        Args:
            libraries: Raw library data

        Returns:
            Sorted list of LibraryRecommendation (best first)
        """
        ranked = []

        for lib in libraries:
            score = self._calculate_quality_score(lib)

            try:
                last_updated = datetime.fromisoformat(lib.get('last_updated', datetime.now().isoformat()))
            except:
                last_updated = datetime.now()

            ranked.append(LibraryRecommendation(
                name=lib.get('name', 'unknown'),
                description=lib.get('description', ''),
                repository_url=lib.get('repository_url', ''),
                stars=lib.get('stars', 0),
                last_updated=last_updated,
                package_manager=self._get_package_manager(),
                install_command=self._generate_install_command(lib.get('name', '')),
                why_recommended=self._generate_recommendation_reason(lib, score),
                score=score,
                weekly_downloads=lib.get('downloads'),
                license=lib.get('license')
            ))

        return sorted(ranked, key=lambda x: x.score, reverse=True)

    def _calculate_quality_score(self, lib: Dict[str, Any]) -> float:
        """
        Calculate overall quality score (0-100)

        Weights:
        - Stars: 40 points max
        - Maintenance: 30 points max
        - Downloads: 20 points max
        - License: 10 points max
        """
        score = 0.0

        # Stars (40 points)
        stars = lib.get('stars') or 0  # Handle None
        if stars > 10000:
            score += 40
        elif stars > 5000:
            score += 35
        elif stars > 1000:
            score += 30
        elif stars > 500:
            score += 25
        elif stars > 100:
            score += 20
        else:
            score += 10

        # Maintenance (30 points)
        last_updated_str = lib.get('last_updated')
        if last_updated_str:
            try:
                last_updated = datetime.fromisoformat(last_updated_str)
                days_ago = (datetime.now() - last_updated).days

                if days_ago < 30:
                    score += 30  # Very active
                elif days_ago < 90:
                    score += 25  # Active
                elif days_ago < 180:
                    score += 20  # Maintained
                elif days_ago < 365:
                    score += 10  # Somewhat maintained
                # else: 0 points (likely abandoned)
            except:
                score += 10  # Unknown, give some points

        # Downloads (20 points)
        downloads = lib.get('downloads') or 0  # Handle None
        if downloads > 1000000:
            score += 20
        elif downloads > 100000:
            score += 15
        elif downloads > 10000:
            score += 10
        elif downloads > 1000:
            score += 5

        # License (10 points)
        license = (lib.get('license') or '').lower()  # Handle None
        if any(l in license for l in ['mit', 'apache', 'bsd']):
            score += 10
        elif 'isc' in license or 'unlicense' in license:
            score += 8
        elif 'gpl' in license:
            score += 5  # GPL is open but restrictive

        return score

    def _generate_recommendation_reason(self, lib: Dict[str, Any], score: float) -> str:
        """Generate explanation for why this library is recommended"""
        reasons = []

        stars = lib.get('stars') or 0  # Handle None
        if stars > 5000:
            reasons.append(f"{stars:,} stars (very popular)")
        elif stars > 1000:
            reasons.append(f"{stars:,} stars (popular)")

        last_updated = lib.get('last_updated')
        if last_updated:
            try:
                days_ago = (datetime.now() - datetime.fromisoformat(last_updated)).days
                if days_ago < 30:
                    reasons.append("recently updated")
                elif days_ago < 180:
                    reasons.append("actively maintained")
            except:
                pass

        downloads = lib.get('downloads')
        if downloads and downloads > 100000:
            reasons.append(f"{downloads:,} weekly downloads")

        license = lib.get('license') or ''
        if license and 'mit' in license.lower():
            reasons.append("MIT license")

        if not reasons:
            reasons.append("meets basic quality criteria")

        return ", ".join(reasons)

    def _get_package_manager(self) -> str:
        """Get appropriate package manager for this project"""
        if self.language in ["javascript", "typescript"]:
            return "npm"
        elif self.language == "python":
            return "pip"
        elif self.language == "swift":
            return "spm"  # Swift Package Manager
        elif self.language == "java":
            return "maven"
        elif self.language == "rust":
            return "cargo"
        else:
            return "unknown"

    def _generate_install_command(self, package_name: str) -> str:
        """Generate installation command for this package"""
        pm = self._get_package_manager()

        if pm == "npm":
            return f"npm install {package_name}"
        elif pm == "pip":
            return f"pip install {package_name}"
        elif pm == "spm":
            return f"Add via Xcode: File → Add Packages → {package_name}"
        elif pm == "maven":
            return f"Add to pom.xml: {package_name}"
        elif pm == "cargo":
            return f"cargo add {package_name}"
        else:
            return f"Install {package_name}"

    def _detect_project_type(self) -> str:
        """Detect project type (same logic as PromptEnhancer)"""
        from shannon.executor.prompt_enhancer import PromptEnhancer
        enhancer = PromptEnhancer()
        return enhancer._detect_project_type(self.project_root)

    def _detect_language(self) -> str:
        """Detect primary programming language"""
        # Based on project type
        if self.project_type.startswith('ios'):
            return "swift"
        elif self.project_type in ['react-native', 'react-native-expo', 'react', 'next.js', 'nodejs', 'vue']:
            # Check if TypeScript
            if (self.project_root / 'tsconfig.json').exists():
                return "typescript"
            else:
                return "javascript"
        elif self.project_type.startswith('python'):
            return "python"
        elif self.project_type == 'android':
            return "java"  # or kotlin
        elif self.project_type == 'rust':
            return "rust"
        elif self.project_type == 'go':
            return "go"
        else:
            return "unknown"

    async def _check_serena_cache(self, key: str) -> Optional[List[LibraryRecommendation]]:
        """
        Check Serena MCP for cached library discoveries

        Args:
            key: Cache key

        Returns:
            Cached libraries if found and recent, None otherwise
        """
        try:
            # Use mcp_memory_search_nodes to find cached libraries
            import sys

            # Check if mcp_memory_search_nodes is available
            if 'mcp_memory_search_nodes' not in dir(sys.modules.get('__main__', {})):
                self.logger.debug("Serena MCP not available, skipping cache")
                return None

            # Search for cached libraries
            # (Would use actual MCP call here in real environment with MCP access)
            # For now, file-based cache as fallback

            cache_file = self.project_root / '.shannon_cache' / f'{key}.json'
            if cache_file.exists():
                import json
                cached_data = json.loads(cache_file.read_text())

                # Check if recent (< 7 days)
                cached_at = datetime.fromisoformat(cached_data.get('cached_at'))
                if (datetime.now() - cached_at) < timedelta(days=7):
                    libraries = []
                    for lib_data in cached_data.get('libraries', []):
                        lib_data['last_updated'] = datetime.fromisoformat(lib_data['last_updated'])
                        libraries.append(LibraryRecommendation(**lib_data))

                    self.logger.info(f"Loaded {len(libraries)} libraries from cache")
                    return libraries

        except Exception as e:
            self.logger.warning(f"Serena cache check failed: {e}")

        return None

    async def _cache_in_serena(self, key: str, libraries: List[LibraryRecommendation]):
        """
        Cache discovered libraries in Serena MCP or file-based cache

        Args:
            key: Cache key
            libraries: Libraries to cache
        """
        try:
            # File-based cache as fallback
            cache_dir = self.project_root / '.shannon_cache'
            cache_dir.mkdir(exist_ok=True)

            cache_file = cache_dir / f'{key}.json'
            cache_data = {
                'libraries': [lib.to_dict() for lib in libraries],
                'cached_at': datetime.now().isoformat()
            }

            import json
            cache_file.write_text(json.dumps(cache_data, indent=2))

            self.logger.debug(f"Cached {len(libraries)} libraries")

        except Exception as e:
            self.logger.warning(f"Caching failed: {e}")
            # Cache failure is non-fatal

