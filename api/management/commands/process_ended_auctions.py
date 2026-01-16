from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

from api.models import AuctionItem, ItemBid

class Command(BaseCommand):
    help = "Find ended auctions, determine winner, send confirmation email"

    @transaction.atomic
    def handle(self, *args, **options):
        now = timezone.now()

        ended = (
            AuctionItem.objects
            .select_for_update()
            .filter(end_datetime__lte=now, ended_processed=False)
        )

        count = 0
        for item in ended:
            top_bid = (
                ItemBid.objects
                .filter(item=item)
                .order_by("-amount", "timestamp")
                .first()
            )

            if not top_bid:
                item.ended_processed = True
                item.save(update_fields=["ended_processed"])
                continue

            winner = top_bid.bidder
            item.winner = winner
            item.winning_bid = top_bid.amount

            subject = f"You won the auction: {item.title}"
            message = (
                f"Hi {winner.username},\n\n"
                f"Congratulations! You won the auction for '{item.title}'.\n"
                f"Winning bid: £{top_bid.amount}\n\n"
                f"Please proceed to purchase the item by logging into the site.\n\n"
                f"Thanks,\nAuction Team"
            )

            if winner.email:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [winner.email],
                    fail_silently=False,
                )
                item.winner_notified_at = timezone.now()

            item.ended_processed = True
            item.save(update_fields=["winner", "winning_bid", "winner_notified_at", "ended_processed"])
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Processed {count} ended auctions."))
