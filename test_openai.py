from openai import OpenAI

client = OpenAI(api_key="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")

try:
    result = client.images.generate(
        model="gpt-image-1",
        prompt="A cartoon of a child brushing teeth",
        size="512x512"
    )
    print("✅ Success! Here's your image URL:")
    print(result.data[0].url)
except Exception as e:
    print("❌ Error:", e)
