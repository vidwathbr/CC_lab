from locust import task, run_single_user, FastHttpUser
import logging


class Browse(FastHttpUser):
    host = "http://localhost:5000"  # Ensure this is the correct backend URL

    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
    }

    @task
    def browse(self):
        """
        Simulates a browsing action by sending a GET request to the /browse endpoint.
        """
        with self.client.get(
            "/browse",
            headers=self.default_headers,
            timeout=2.0,  # Explicitly set a 2-second timeout
            catch_response=True,
        ) as response:
            # Get the response time in milliseconds
            response_time_ms = response.request_meta.get("response_time", 0)

            # Check response time and status code
            if response.status_code == 200 and response_time_ms < 2000:
                response.success()
            else:
                logging.warning(
                    f"High response time: {response_time_ms}ms | Status: {response.status_code}"
                )
                response.failure(
                    f"Failed with status code: {response.status_code}, "
                    f"Response time: {response_time_ms}ms"
                )


if __name__ == "__main__":
    run_single_user(Browse)
