# StoryVerse Research

## TODO

* [x] API rate limits, RPM ,cost
* [ ] Fall back API/method
* [ ] Database (size/type of data to be stored/maintenance)-books,photos,user data
* [ ] Request queueing mechanism
* [ ] Azure VM vs Azure services cost and effort (load balancing/scaling/maintaining redis/database)
* [ ] CPU/GPU/RAM requirements for 1000 user site
* [ ] Payment handling

### API Rate Limits, Cost

* All Azure pricing is with respect to 100 images
* Go through Chatgpt Usage Tiers as well

Reference: 
* [Rate Limits](https://platform.openai.com/settings/organization/limits) 
* [Cost](https://platform.openai.com/docs/pricing)
* [Azure](https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits?tabs=REST#batch-limits)

#### Dall-e-2

* OpenAI

    * 500 Requests per minute or 5 images per minute (whichever occurs first)

    * Pricing

    * Standard Quality
        * 256x256   -> $0.016
        * 512x512   -> $0.018
        * 1024x1024 -> $0.02

* Azure

    * Default DALL-E 2 -> 2 concurrent requests
    
    * Pricing
        
        * Standard
            * 1024x1024 -> $2
    
#### Dall-e-3

* OpenAI 

    * 500 Requests per minute or 5 images per minute (whichever occurs first)

    * Pricing

        * Standard Quality
            * 1024x1024 -> $0.04
            * 1024x1792 -> $0.08
            * 1792x1024 -> $0.08

        * HD Quality
            * 1024x1024 -> $0.08
            * 1024x1792 -> $0.12
            * 1792x1024 -> $0.12

* Azure

    * Default DALL-E 3 -> 2 capacity units (6 requests per minute)

    * Pricing

        * Standard Quality
            * 1024x1024 -> $4
            * 1024x1792 -> $8
            * 1792x1024 -> $8

        * HD Quality
            * 1024x1024 -> $8
            * 1024x1792 -> $12
            * 1792x1024 -> $12

#### gpt-image-1

* OpenAI

    * 40000 tokens per minute or 5 images per minute (whichever occurs first)

    * Pricing

    * Low Quality
        * 1024x0124 -> $0.011
        * 1024x1536 -> $0.016
        * 1536x1024 -> $0.016

    * Medium Quality
        * 1024x0124 -> $0.042
        * 1024x1536 -> $0.063
        * 1536x1024 -> $0.063

    * High Quality
        * 1024x0124 -> $0.167
        * 1024x1536 -> $0.25
        * 1536x1024 -> $0.25

    * Please note that this pricing for GPT Image 1 does not include text and image tokens used in the image generation process, and only reflects the output image tokens cost. There are no additional costs for DALL·E 2 or DALL·E 3.

* Azure

    * Default GPT-image-1 -> 2 capacity units (6 requests per minute)
    
    * No pricing information has been specified anywhere

### Fallback API or Method
