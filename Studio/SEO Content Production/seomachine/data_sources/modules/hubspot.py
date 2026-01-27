"""
HubSpot CRM Analytics Integration

Fetches contacts, forms, lists, and analytics data from HubSpot API.
Provides attribution, funnel, and Curriculove-specific analytics.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import Counter


class HubSpotAnalytics:
    """HubSpot API client for CRM analytics"""

    BASE_URL = "https://api.hubapi.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        portal_id: Optional[str] = None
    ):
        """
        Initialize HubSpot client

        Args:
            api_key: HubSpot API key (defaults to env var HUBSPOT_API_KEY)
            portal_id: HubSpot Portal ID (defaults to env var HUBSPOT_PORTAL_ID)
        """
        self.api_key = api_key or os.getenv('HUBSPOT_API_KEY')
        self.portal_id = portal_id or os.getenv('HUBSPOT_PORTAL_ID')

        if not self.api_key:
            raise ValueError("HUBSPOT_API_KEY must be provided or set in environment")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _request(self, endpoint: str, method: str = 'GET', params: Optional[Dict] = None, data: Optional[Dict] = None) -> Optional[Dict]:
        """Make authenticated request to HubSpot API"""
        url = f"{self.BASE_URL}{endpoint}"

        if method == 'GET':
            response = requests.get(url, headers=self.headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=self.headers, params=params, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        if response.status_code == 200:
            return response.json()
        else:
            error_msg = response.json().get('message', response.text) if response.text else f"Status {response.status_code}"
            raise Exception(f"HubSpot API error ({response.status_code}): {error_msg}")

    # ========== DISCOVERY METHODS ==========

    def get_contact_properties(self) -> List[Dict[str, Any]]:
        """
        Get all contact properties (custom and HubSpot-defined)

        Returns:
            List of property dicts with name, label, type, description
        """
        data = self._request("/crm/v3/properties/contacts")
        if not data:
            return []

        properties = []
        for prop in data.get("results", []):
            properties.append({
                "name": prop.get("name"),
                "label": prop.get("label"),
                "type": prop.get("type"),
                "description": prop.get("description", ""),
                "hubspot_defined": prop.get("hubspotDefined", False),
                "options": [o.get("value") for o in prop.get("options", [])]
            })

        return properties

    def get_custom_properties(self) -> List[Dict[str, Any]]:
        """Get only custom (non-HubSpot) properties"""
        return [p for p in self.get_contact_properties() if not p['hubspot_defined']]

    def get_forms(self) -> List[Dict[str, Any]]:
        """
        Get all marketing forms

        Returns:
            List of form dicts with id, name, type, fields
        """
        data = self._request("/marketing/v3/forms")
        if not data:
            return []

        forms = []
        for form in data.get("results", []):
            field_names = []
            for group in form.get("fieldGroups", []):
                for field in group.get("fields", []):
                    field_names.append(field.get("name"))

            forms.append({
                "id": form.get("id"),
                "name": form.get("name"),
                "type": form.get("formType"),
                "created_at": form.get("createdAt"),
                "updated_at": form.get("updatedAt"),
                "fields": field_names,
            })

        return forms

    def get_lists(self) -> List[Dict[str, Any]]:
        """
        Get contact lists with member counts

        Returns:
            List of list dicts with id, name, count, type
        """
        # Try legacy lists API first
        data = self._request("/contacts/v1/lists", params={"count": 250})

        if not data:
            return []

        lists = []
        for lst in data.get("lists", []):
            lists.append({
                "id": lst.get("listId"),
                "name": lst.get("name"),
                "count": lst.get("metaData", {}).get("size", 0),
                "type": lst.get("listType"),
                "created_at": lst.get("createdAt"),
                "dynamic": lst.get("dynamic", False),
            })

        return sorted(lists, key=lambda x: -x['count'])

    # ========== CONTACTS & ATTRIBUTION ==========

    def _get_contacts_batch(
        self,
        properties: List[str],
        limit: int = 100,
        after: Optional[str] = None,
        filters: Optional[List[Dict]] = None
    ) -> tuple:
        """Get a batch of contacts with pagination"""
        params = {
            "limit": limit,
            "properties": ",".join(properties),
        }
        if after:
            params["after"] = after

        if filters:
            # Use search endpoint for filtering
            data = self._request("/crm/v3/objects/contacts/search", method='POST', data={
                "filterGroups": [{"filters": filters}],
                "properties": properties,
                "limit": limit,
                "after": after,
            })
        else:
            data = self._request("/crm/v3/objects/contacts", params=params)

        if not data:
            return [], None

        contacts = data.get("results", [])
        paging = data.get("paging", {})
        next_after = paging.get("next", {}).get("after")

        return contacts, next_after

    def get_contacts(
        self,
        properties: Optional[List[str]] = None,
        days: int = 30,
        max_contacts: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Get contacts created within specified days

        Args:
            properties: List of property names to fetch
            days: Number of days to look back
            max_contacts: Maximum contacts to return

        Returns:
            List of contact dicts
        """
        if properties is None:
            properties = [
                "email", "firstname", "lastname", "createdate",
                "hs_analytics_source", "hs_analytics_source_data_1", "hs_analytics_source_data_2",
                "hs_analytics_first_url", "hs_analytics_first_referrer",
                "first_conversion_event_name", "recent_conversion_event_name",
                "lifecyclestage", "hs_lead_status",
            ]

        since_date = datetime.now() - timedelta(days=days)
        since_ms = int(since_date.timestamp() * 1000)

        all_contacts = []
        after = None
        batches = (max_contacts // 100) + 1

        for _ in range(batches):
            if len(all_contacts) >= max_contacts:
                break

            contacts, after = self._get_contacts_batch(
                properties=properties,
                limit=100,
                after=after,
                filters=[{
                    "propertyName": "createdate",
                    "operator": "GTE",
                    "value": str(since_ms)
                }]
            )

            all_contacts.extend(contacts)
            if not after:
                break

        return all_contacts[:max_contacts]

    def get_contacts_by_source(self, days: int = 30, max_contacts: int = 1000) -> Dict[str, int]:
        """
        Get contact counts by analytics source

        Args:
            days: Number of days to look back
            max_contacts: Maximum contacts to analyze

        Returns:
            Dict mapping source to count (e.g., {'ORGANIC_SEARCH': 150, 'PAID_SOCIAL': 45})
        """
        contacts = self.get_contacts(
            properties=["hs_analytics_source"],
            days=days,
            max_contacts=max_contacts
        )

        sources = Counter()
        for contact in contacts:
            source = contact.get("properties", {}).get("hs_analytics_source", "UNKNOWN")
            sources[source] += 1

        return dict(sources.most_common())

    def get_contacts_by_source_detail(self, days: int = 30, max_contacts: int = 1000) -> Dict[str, Dict[str, int]]:
        """
        Get contact counts by source and source detail

        Returns:
            Nested dict: {'ORGANIC_SEARCH': {'google': 100, 'bing': 20}}
        """
        contacts = self.get_contacts(
            properties=["hs_analytics_source", "hs_analytics_source_data_1"],
            days=days,
            max_contacts=max_contacts
        )

        sources = {}
        for contact in contacts:
            props = contact.get("properties", {})
            source = props.get("hs_analytics_source", "UNKNOWN")
            detail = props.get("hs_analytics_source_data_1", "unknown")

            if source not in sources:
                sources[source] = Counter()
            sources[source][detail] += 1

        return {k: dict(v.most_common()) for k, v in sources.items()}

    def get_contacts_by_lifecycle(self, days: int = 30, max_contacts: int = 1000) -> Dict[str, int]:
        """
        Get contact counts by lifecycle stage

        Returns:
            Dict mapping stage to count (e.g., {'subscriber': 500, 'lead': 150})
        """
        contacts = self.get_contacts(
            properties=["lifecyclestage"],
            days=days,
            max_contacts=max_contacts
        )

        stages = Counter()
        for contact in contacts:
            stage = contact.get("properties", {}).get("lifecyclestage", "unknown")
            stages[stage] += 1

        return dict(stages.most_common())

    def get_landing_page_conversions(self, days: int = 30, max_contacts: int = 1000) -> List[Dict[str, Any]]:
        """
        Get contact counts by first landing page URL

        Returns:
            List of dicts with url, count, top_source
        """
        contacts = self.get_contacts(
            properties=["hs_analytics_first_url", "hs_analytics_source"],
            days=days,
            max_contacts=max_contacts
        )

        pages = {}
        for contact in contacts:
            props = contact.get("properties", {})
            url = props.get("hs_analytics_first_url", "")
            source = props.get("hs_analytics_source", "UNKNOWN")

            if not url:
                continue

            # Clean URL - remove query params for grouping
            clean_url = url.split("?")[0] if url else ""

            if clean_url not in pages:
                pages[clean_url] = {"count": 0, "sources": Counter()}
            pages[clean_url]["count"] += 1
            pages[clean_url]["sources"][source] += 1

        result = []
        for url, data in pages.items():
            top_source = data["sources"].most_common(1)
            result.append({
                "url": url,
                "count": data["count"],
                "top_source": top_source[0][0] if top_source else "UNKNOWN",
            })

        return sorted(result, key=lambda x: -x["count"])

    def get_form_conversions(self, days: int = 30, max_contacts: int = 1000) -> Dict[str, int]:
        """
        Get contact counts by first conversion form

        Returns:
            Dict mapping form name to count
        """
        contacts = self.get_contacts(
            properties=["first_conversion_event_name"],
            days=days,
            max_contacts=max_contacts
        )

        forms = Counter()
        for contact in contacts:
            form = contact.get("properties", {}).get("first_conversion_event_name", "")
            if form:
                forms[form] += 1

        return dict(forms.most_common())

    # ========== CURRICULOVE SPECIFIC ==========

    def get_curriculove_leads(self, days: int = 30, max_contacts: int = 1000) -> Dict[str, Any]:
        """
        Get Curriculove quiz leads with philosophy data

        Returns:
            Dict with total, by_philosophy, by_confidence, recent_contacts
        """
        curriculove_properties = [
            "email", "createdate",
            "curriculove_primary_philosophy", "curriculove_philosophy_name",
            "curriculove_secondary_philosophies", "curriculove_confidence",
            "curriculove_quiz_date", "state",
            "hs_analytics_source",
        ]

        contacts = self.get_contacts(
            properties=curriculove_properties,
            days=days,
            max_contacts=max_contacts
        )

        # Filter to only Curriculove contacts
        curriculove_contacts = []
        for contact in contacts:
            props = contact.get("properties", {})
            if props.get("curriculove_primary_philosophy") or props.get("curriculove_quiz_date"):
                curriculove_contacts.append(contact)

        by_philosophy = Counter()
        by_confidence = Counter()
        by_state = Counter()
        by_source = Counter()

        for contact in curriculove_contacts:
            props = contact.get("properties", {})
            philosophy = props.get("curriculove_philosophy_name") or props.get("curriculove_primary_philosophy", "unknown")
            confidence = props.get("curriculove_confidence", "unknown")
            state = props.get("state", "unknown")
            source = props.get("hs_analytics_source", "unknown")

            by_philosophy[philosophy] += 1
            by_confidence[confidence] += 1
            by_state[state] += 1
            by_source[source] += 1

        return {
            "total": len(curriculove_contacts),
            "by_philosophy": dict(by_philosophy.most_common()),
            "by_confidence": dict(by_confidence.most_common()),
            "by_state": dict(by_state.most_common()),
            "by_source": dict(by_source.most_common()),
        }

    def get_leads_by_philosophy(self, days: int = 30, max_contacts: int = 1000) -> Dict[str, int]:
        """Get contact counts by Curriculove philosophy"""
        data = self.get_curriculove_leads(days=days, max_contacts=max_contacts)
        return data.get("by_philosophy", {})

    def get_leads_by_state(self, days: int = 30, max_contacts: int = 1000) -> Dict[str, int]:
        """
        Get contact counts by state

        Returns:
            Dict mapping state to count
        """
        contacts = self.get_contacts(
            properties=["state"],
            days=days,
            max_contacts=max_contacts
        )

        states = Counter()
        for contact in contacts:
            state = contact.get("properties", {}).get("state", "")
            if state:
                states[state] += 1

        return dict(states.most_common())

    # ========== FUNNEL ANALYTICS ==========

    def get_funnel_conversion_rates(self, days: int = 30, max_contacts: int = 5000) -> Dict[str, Any]:
        """
        Calculate funnel conversion rates

        Returns:
            Dict with stage counts and conversion rates
        """
        contacts = self.get_contacts(
            properties=["lifecyclestage", "hs_analytics_source"],
            days=days,
            max_contacts=max_contacts
        )

        stages = Counter()
        for contact in contacts:
            stage = contact.get("properties", {}).get("lifecyclestage", "unknown")
            stages[stage] += 1

        total = len(contacts)
        subscribers = stages.get("subscriber", 0)
        leads = stages.get("lead", 0)
        mqls = stages.get("marketingqualifiedlead", 0)
        customers = stages.get("customer", 0)

        return {
            "total_contacts": total,
            "stages": {
                "subscriber": subscribers,
                "lead": leads,
                "mql": mqls,
                "customer": customers,
            },
            "conversion_rates": {
                "subscriber_to_lead": round(leads / subscribers * 100, 1) if subscribers > 0 else 0,
                "lead_to_mql": round(mqls / leads * 100, 1) if leads > 0 else 0,
                "mql_to_customer": round(customers / mqls * 100, 1) if mqls > 0 else 0,
                "subscriber_to_customer": round(customers / subscribers * 100, 1) if subscribers > 0 else 0,
            }
        }

    def get_source_to_lead_rate(self, days: int = 30, max_contacts: int = 5000) -> Dict[str, Dict[str, Any]]:
        """
        Calculate lead conversion rate by source

        Returns:
            Dict with source -> {total, leads, rate}
        """
        contacts = self.get_contacts(
            properties=["lifecyclestage", "hs_analytics_source"],
            days=days,
            max_contacts=max_contacts
        )

        sources = {}
        for contact in contacts:
            props = contact.get("properties", {})
            source = props.get("hs_analytics_source", "UNKNOWN")
            stage = props.get("lifecyclestage", "unknown")

            if source not in sources:
                sources[source] = {"total": 0, "leads": 0}
            sources[source]["total"] += 1
            if stage in ["lead", "marketingqualifiedlead", "customer"]:
                sources[source]["leads"] += 1

        for source, data in sources.items():
            data["rate"] = round(data["leads"] / data["total"] * 100, 1) if data["total"] > 0 else 0

        return dict(sorted(sources.items(), key=lambda x: -x[1]["total"]))

    # ========== TIME-BASED ANALYTICS ==========

    def get_weekly_signups(self, weeks: int = 12) -> List[Dict[str, Any]]:
        """
        Get weekly signup counts

        Returns:
            List of dicts with week_start, count
        """
        days = weeks * 7
        contacts = self.get_contacts(
            properties=["createdate"],
            days=days,
            max_contacts=10000
        )

        weekly = Counter()
        for contact in contacts:
            created = contact.get("properties", {}).get("createdate", "")
            if created:
                try:
                    date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    week_start = date - timedelta(days=date.weekday())
                    week_key = week_start.strftime("%Y-%m-%d")
                    weekly[week_key] += 1
                except (ValueError, TypeError):
                    pass

        return [{"week_start": k, "count": v} for k, v in sorted(weekly.items())]

    def get_monthly_signups(self, months: int = 6) -> List[Dict[str, Any]]:
        """
        Get monthly signup counts

        Returns:
            List of dicts with month, count
        """
        days = months * 30
        contacts = self.get_contacts(
            properties=["createdate"],
            days=days,
            max_contacts=10000
        )

        monthly = Counter()
        for contact in contacts:
            created = contact.get("properties", {}).get("createdate", "")
            if created:
                try:
                    date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                    month_key = date.strftime("%Y-%m")
                    monthly[month_key] += 1
                except (ValueError, TypeError):
                    pass

        return [{"month": k, "count": v} for k, v in sorted(monthly.items())]

    # ========== EMAIL CAMPAIGNS ==========

    def get_email_campaigns(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all email campaigns with stats

        Returns:
            List of campaign dicts with id, name, sent, opens, clicks, etc.
        """
        data = self._request("/email/public/v1/campaigns", params={"limit": limit})
        if not data:
            return []

        campaigns = []
        for c in data.get("campaigns", []):
            cid = c.get("id")
            # Get detailed stats for each campaign
            stats = self._request(f"/email/public/v1/campaigns/{cid}")
            if stats:
                counters = stats.get("counters", {})
                sent = counters.get("sent", 0)
                opens = counters.get("open", 0)
                clicks = counters.get("click", 0)

                campaigns.append({
                    "id": cid,
                    "name": stats.get("name", "Untitled"),
                    "subject": stats.get("subject", ""),
                    "type": stats.get("type", ""),
                    "sent": sent,
                    "opens": opens,
                    "clicks": clicks,
                    "bounces": counters.get("bounce", 0),
                    "unsubscribes": counters.get("unsubscribed", 0),
                    "open_rate": round(opens / sent * 100, 1) if sent > 0 else 0,
                    "click_rate": round(clicks / sent * 100, 1) if sent > 0 else 0,
                })

        return campaigns

    def get_email_stats_summary(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get aggregate email stats across recent campaigns

        Returns:
            Dict with totals, averages, and top performers
        """
        campaigns = self.get_email_campaigns(limit=limit)

        totals = {
            "campaigns": len(campaigns),
            "sent": sum(c["sent"] for c in campaigns),
            "opens": sum(c["opens"] for c in campaigns),
            "clicks": sum(c["clicks"] for c in campaigns),
            "bounces": sum(c["bounces"] for c in campaigns),
            "unsubscribes": sum(c["unsubscribes"] for c in campaigns),
        }

        totals["avg_open_rate"] = round(totals["opens"] / totals["sent"] * 100, 1) if totals["sent"] > 0 else 0
        totals["avg_click_rate"] = round(totals["clicks"] / totals["sent"] * 100, 1) if totals["sent"] > 0 else 0

        # Top performers by open rate (min 100 sent)
        qualified = [c for c in campaigns if c["sent"] >= 100]
        top_by_opens = sorted(qualified, key=lambda x: -x["open_rate"])[:5]
        top_by_clicks = sorted(qualified, key=lambda x: -x["click_rate"])[:5]

        return {
            "totals": totals,
            "top_by_open_rate": top_by_opens,
            "top_by_click_rate": top_by_clicks,
        }

    def get_email_click_events(self, campaign_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get click events for a specific campaign (which links were clicked)

        Args:
            campaign_id: HubSpot campaign ID
            limit: Max events to return

        Returns:
            List of click events with url, recipient, timestamp
        """
        data = self._request(
            "/email/public/v1/events",
            params={"campaignId": campaign_id, "eventType": "CLICK", "limit": limit}
        )
        if not data:
            return []

        events = []
        for e in data.get("events", []):
            events.append({
                "url": e.get("url", ""),
                "recipient": e.get("recipient", ""),
                "timestamp": e.get("created", ""),
            })

        return events

    def get_link_click_summary(self, campaign_id: str) -> Dict[str, int]:
        """
        Get click counts by URL for a campaign

        Returns:
            Dict mapping URL to click count
        """
        events = self.get_email_click_events(campaign_id, limit=500)
        url_counts = Counter()
        for e in events:
            url = e.get("url", "unknown")
            # Clean tracking params for grouping
            clean_url = url.split("?")[0] if "?" in url else url
            url_counts[clean_url] += 1

        return dict(url_counts.most_common())

    # ========== SUBSCRIPTION PREFERENCES ==========

    def get_subscription_types(self) -> List[Dict[str, Any]]:
        """
        Get all subscription types (email preferences)

        Returns:
            List of subscription type dicts
        """
        data = self._request("/communication-preferences/v3/definitions")
        if not data:
            return []

        return [
            {
                "id": s.get("id"),
                "name": s.get("name"),
                "description": s.get("description", ""),
                "purpose": s.get("purpose", ""),
                "is_active": s.get("isActive", True),
            }
            for s in data.get("subscriptionDefinitions", [])
        ]

    def get_contact_subscriptions(self, email: str) -> Dict[str, Any]:
        """
        Get subscription status for a contact

        Args:
            email: Contact email address

        Returns:
            Dict with subscription statuses
        """
        data = self._request(f"/communication-preferences/v3/status/email/{email}")
        if not data:
            return {}

        return {
            "recipient": data.get("recipient", email),
            "subscription_statuses": [
                {
                    "id": s.get("id"),
                    "name": s.get("name"),
                    "status": s.get("status"),  # SUBSCRIBED, NOT_SUBSCRIBED, etc.
                }
                for s in data.get("subscriptionStatuses", [])
            ]
        }

    # ========== ENHANCED LISTS ==========

    def get_list_members(self, list_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get contacts in a specific list

        Args:
            list_id: HubSpot list ID
            limit: Max contacts to return

        Returns:
            List of contact dicts
        """
        data = self._request(
            f"/contacts/v1/lists/{list_id}/contacts/all",
            params={"count": limit, "property": ["email", "firstname", "lastname", "createdate"]}
        )
        if not data:
            return []

        return [
            {
                "vid": c.get("vid"),
                "email": c.get("properties", {}).get("email", {}).get("value", ""),
                "firstname": c.get("properties", {}).get("firstname", {}).get("value", ""),
                "lastname": c.get("properties", {}).get("lastname", {}).get("value", ""),
            }
            for c in data.get("contacts", [])
        ]

    def get_list_growth(self, list_id: int, days: int = 30) -> Dict[str, Any]:
        """
        Estimate list growth over time (based on member create dates)

        Returns:
            Dict with current_size, new_in_period, growth_rate
        """
        members = self.get_list_members(list_id, limit=500)
        lists = self.get_lists()
        current_list = next((l for l in lists if l["id"] == list_id), None)

        # This is an approximation - HubSpot doesn't track list membership history
        return {
            "list_id": list_id,
            "list_name": current_list["name"] if current_list else "Unknown",
            "current_size": current_list["count"] if current_list else len(members),
            "sample_size": len(members),
        }

    # ========== FORMS ANALYTICS ==========

    def get_form_submissions(self, form_guid: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent submissions for a form

        Args:
            form_guid: Form GUID
            limit: Max submissions to return

        Returns:
            List of submission dicts
        """
        data = self._request(f"/form-integrations/v1/submissions/forms/{form_guid}", params={"limit": limit})
        if not data:
            return []

        submissions = []
        for s in data.get("results", []):
            values = {}
            for field in s.get("values", []):
                values[field.get("name")] = field.get("value")

            submissions.append({
                "submitted_at": s.get("submittedAt"),
                "page_url": s.get("pageUrl", ""),
                "values": values,
            })

        return submissions

    def get_forms_performance(self) -> List[Dict[str, Any]]:
        """
        Get all forms with submission counts

        Returns:
            List of forms with submission metrics
        """
        forms = self.get_forms()
        performance = []

        for form in forms[:20]:  # Limit to avoid rate limits
            try:
                submissions = self.get_form_submissions(form["id"], limit=1)
                # Note: We can't easily get total count, so we just verify the form works
                performance.append({
                    "id": form["id"],
                    "name": form["name"],
                    "type": form["type"],
                    "fields": form["fields"],
                    "has_submissions": len(submissions) > 0,
                })
            except Exception:
                performance.append({
                    "id": form["id"],
                    "name": form["name"],
                    "type": form["type"],
                    "fields": form["fields"],
                    "has_submissions": False,
                })

        return performance

    # ========== DASHBOARD SUMMARY ==========

    def get_dashboard_summary(self, days: int = 30) -> Dict[str, Any]:
        """
        Get combined summary for dashboard

        Returns:
            Dict with overview, sources, funnel, top_pages
        """
        sources = self.get_contacts_by_source(days=days)
        stages = self.get_contacts_by_lifecycle(days=days)
        pages = self.get_landing_page_conversions(days=days)
        forms = self.get_form_conversions(days=days)

        total = sum(sources.values())

        return {
            "generated_at": datetime.now().isoformat(),
            "period_days": days,
            "total_contacts": total,
            "by_source": sources,
            "by_stage": stages,
            "top_landing_pages": pages[:10],
            "top_forms": dict(list(forms.items())[:10]),
        }

    def get_full_marketing_dashboard(self, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive marketing dashboard including email stats

        Returns:
            Dict with CRM data + email campaign performance
        """
        # CRM data
        sources = self.get_contacts_by_source(days=days)
        stages = self.get_contacts_by_lifecycle(days=days)
        pages = self.get_landing_page_conversions(days=days)

        # Email data
        email_stats = self.get_email_stats_summary(limit=30)

        # Lists
        lists = self.get_lists()[:10]

        # Subscription types
        sub_types = self.get_subscription_types()

        total = sum(sources.values())

        return {
            "generated_at": datetime.now().isoformat(),
            "period_days": days,
            "crm": {
                "total_contacts": total,
                "by_source": sources,
                "by_stage": stages,
                "top_landing_pages": pages[:5],
            },
            "email": {
                "totals": email_stats["totals"],
                "top_by_open_rate": email_stats["top_by_open_rate"][:3],
                "top_by_click_rate": email_stats["top_by_click_rate"][:3],
            },
            "lists": lists,
            "subscription_types": len(sub_types),
        }


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('data_sources/config/.env')

    hs = HubSpotAnalytics()

    print("HubSpot Dashboard Summary (Last 30 Days)")
    print("=" * 50)

    summary = hs.get_dashboard_summary()

    print(f"\nTotal Contacts: {summary['total_contacts']:,}")

    print("\nBy Source:")
    for source, count in summary['by_source'].items():
        print(f"  {source}: {count}")

    print("\nBy Stage:")
    for stage, count in summary['by_stage'].items():
        print(f"  {stage}: {count}")

    print("\nTop Landing Pages:")
    for page in summary['top_landing_pages'][:5]:
        print(f"  {page['url'][:60]}: {page['count']}")
