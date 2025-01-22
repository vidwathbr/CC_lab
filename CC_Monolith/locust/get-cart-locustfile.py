from locust import task, run_single_user, FastHttpUser
from insert_product import login
import logging


class AddToCart(FastHttpUser):
    host = "http://localhost:5000"  # Replace with your actual host
    username = "test123"
    password = "test123"
    token = None  # Initialize token as None

    def on_start(self):
        """
        This method is called when a simulated user starts.
        Use it to handle login and setup tasks.
        """
        cookies = login(self.username, self.password)

        if cookies and "token" in cookies:
            self.token = cookies.get("token")
            self.default_headers = {
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "DNT": "1",
                "Sec-GPC": "1",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
                "Upgrade-Insecure-Requests": "1",
            }
        else:
            logging.error("Failed to retrieve token from login.")
            self.token = None
            self.default_headers = {}

    @task
    def view_cart(self):
        """
        Simulates viewing the cart.
        """
        if not self.token:
            logging.error("Token not available. Skipping the task.")
            return

        # Perform the GET request
        with self.client.get(
            "/cart",
            headers=self.default_headers,
            cookies={"token": self.token},
            catch_response=True,
        ) as response:
            response_time_ms = response.request_meta.get("response_time", 0)

            # Validate response time and status code
            if response.status_code == 200 and response_time_ms < 2500:
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
    run_single_user(AddToCart)
