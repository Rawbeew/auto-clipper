import os
import json
import urllib.request
import base64
from nacl import public, encoding

class SocialAuthHelper:
    """
    Assists in generating and setting OAuth secrets for YouTube Shorts, 
    TikTok Content Posting API, and Instagram Reels Graph API.
    Auto-encrypts and uploads tokens to GitHub Actions Secrets.
    """
    def __init__(self, github_repo="Rawbeew/auto-clipper", github_token=None):
        self.github_repo = github_repo
        self.github_token = github_token or os.getenv("GH_PAT", "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")

    def upload_secret_to_github(self, secret_name: str, secret_value: str) -> bool:
        """
        Encrypts secret with Libsodium SealedBox and saves to GitHub Actions.
        """
        try:
            # 1. Fetch Repo Public Key
            url_pk = f"https://api.github.com/repos/{self.github_repo}/actions/secrets/public-key"
            req_pk = urllib.request.Request(url_pk, headers={
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "AutoClipper-SocialSetup"
            })
            with urllib.request.urlopen(req_pk) as resp:
                key_info = json.loads(resp.read().decode("utf-8"))

            key_id = key_info["key_id"]
            public_key_b64 = key_info["key"]

            # 2. Encrypt
            pk = public.PublicKey(public_key_b64.encode('utf-8'), encoding.Base64Encoder())
            sealed_box = public.SealedBox(pk)
            encrypted = sealed_box.encrypt(secret_value.encode('utf-8'))
            enc_b64 = base64.b64encode(encrypted).decode('utf-8')

            # 3. Save
            url_sec = f"https://api.github.com/repos/{self.github_repo}/actions/secrets/{secret_name}"
            payload = json.dumps({"encrypted_value": enc_b64, "key_id": key_id}).encode("utf-8")

            req_sec = urllib.request.Request(url_sec, data=payload, method="PUT", headers={
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json",
                "User-Agent": "AutoClipper-SocialSetup"
            })
            with urllib.request.urlopen(req_sec) as resp:
                print(f"✅ Successfully set social secret '{secret_name}' in GitHub Actions!")
                return True

        except Exception as e:
            print(f"Error setting GitHub secret '{secret_name}': {e}")
            return False

    def save_social_tokens(self, youtube_token=None, tiktok_token=None, instagram_token=None):
        """
        Saves provided social media tokens directly to GitHub Actions.
        """
        if youtube_token:
            self.upload_secret_to_github("YOUTUBE_OAUTH_TOKEN", youtube_token)
        if tiktok_token:
            self.upload_secret_to_github("TIKTOK_ACCESS_TOKEN", tiktok_token)
        if instagram_token:
            self.upload_secret_to_github("INSTAGRAM_ACCESS_TOKEN", instagram_token)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Social Media Auth Helper")
    parser.add_argument("--yt", type=str, help="YouTube OAuth Token")
    parser.add_argument("--tt", type=str, help="TikTok Access Token")
    parser.add_argument("--ig", type=str, help="Instagram Reels Access Token")
    args = parser.parse_args()

    helper = SocialAuthHelper()
    helper.save_social_tokens(args.yt, args.tt, args.ig)
