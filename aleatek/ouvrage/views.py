from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Aso, AffaireOuvrage, Avis, Ouvrage, Documents, FichierAttache, EntrepriseAffaireOuvrage
from .permissions import IsAdminAuthenticated
from .serializers import AsoSerializer, OuvrageSerializer, DocumentSerializer, FichierAttacheSerializer, \
    AvisSerializer, AffaireOuvrageSerializer, EntrepriseAffaireOuvrageSerializer
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from entreprise.models import Entreprise, Responsable
from Dashbord.models import EntrepriseAffaire
from mission.models import  MissionActive
from commentaire.models import Commentaire

class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AsoSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AsoSerializer
    queryset = Aso.objects.all()
    permission_classes = [IsAdminAuthenticated]


class AffaireOuvrageAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AffaireOuvrageSerializer
    queryset = AffaireOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class OuvrageAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = OuvrageSerializer
    queryset = Ouvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class DocumentSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Documents.objects.all()
    permission_classes = [IsAdminAuthenticated]


class AvisSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = AvisSerializer
    queryset = Avis.objects.all()
    permission_classes = [IsAdminAuthenticated]


class FichierSerializerAdminViewsetAdmin(MultipleSerializerMixin, ModelViewSet):
    serializer_class = FichierAttacheSerializer
    queryset = FichierAttache.objects.all()
    permission_classes = [IsAdminAuthenticated]


class EntrepriseAffaireOuvrageViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = EntrepriseAffaireOuvrageSerializer
    queryset = EntrepriseAffaireOuvrage.objects.all()
    permission_classes = [IsAdminAuthenticated]


class VerifyExistAffaireOuvrage(APIView):
    def get(self, request, id_affaire, id_ouvrage):
        try:
            AffaireOuvrage.objects.get(id_affaire=id_affaire, id_ouvrage=id_ouvrage)
            return Response({'check': True})
        except:
            return Response({'check': False})


class GetAllAffaireOuvrageByAffaire(APIView):
    def get(self, request, id_affaire):
        all_affaire_ouvrage = AffaireOuvrage.objects.filter(id_affaire=id_affaire).values()
        data = []
        for ouvrage in all_affaire_ouvrage:
            final_data = dict(ouvrage)  # Convertir l'objet QueryDict en dictionnaire
            detail_ouvrage = Ouvrage.objects.get(id=ouvrage['id_ouvrage_id'])
            ouvrage_data = model_to_dict(detail_ouvrage)
            final_data['ouvrage'] = ouvrage_data
            data.append(final_data)
        return Response(data)


class VerifyEntrepriseCollabOnOuvrage(APIView):
    def get(self, request, id_entreprise_affaire, id_ouvrage_affaire):
        try:
            EntrepriseAffaireOuvrage.objects.get(affaire_ouvrage=id_ouvrage_affaire,
            affaire_entreprise=id_entreprise_affaire)
            return Response({'check': True})
        except:
            return Response({'check': False})


class AllEntreprisebAssignToAffaireOuvrage(APIView):
    def get(self, request, id_affaire_ouvrage):
        entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(
            affaire_ouvrage=id_affaire_ouvrage).values()
        data = []
        for e_a_o in entreprise_affaire_ouvrage:
            final = dict(e_a_o)
            detailEntrepriseAffaire = EntrepriseAffaire.objects.get(id=e_a_o['affaire_entreprise_id'])
            detailEntreprise = model_to_dict(detailEntrepriseAffaire.entreprise)
            final['entreprise'] = detailEntreprise
            data.append(final)

        return Response(data)


class CodificationASOInCurrent(APIView):
    def get(self, request, id_aso):
        aviss = Avis.objects.all()
        ouvrage = Aso.objects.get(id=id_aso).affaireouvrage
        TabCodifications = []
        for avis in aviss:
            print(avis.id)
            document = avis.id_document
            if document.emetteur.affaire_ouvrage.id == ouvrage.id:
                TabCodifications.append(avis.codification)

        if len(TabCodifications) == 0:
            return Response({'codification': False})

        liste = ['RMQ', 'FA', 'F', 'HM', 'SO', 'VI']
        unique_liste = list(set(TabCodifications))
        codification = unique_liste[0]

        for tu in unique_liste:
            if liste.index(tu) < liste.index(codification):
                codification = tu

        return Response({'codification': codification})


class CodificationASO(APIView):
    def get(self, request, id_aso):
        # aviss = Avis.objects.all()
        TabCodifications = []
        # for avis in aviss:
        #     print(avis.id)
        #     document = avis.id_document
        #     if document.aso.id == id_aso:
        #         TabCodifications.append(avis.codification)
        documents = Documents.objects.filter(aso=id_aso)
        for document in documents:
            aviss = Avis.objects.filter(id_document=document.id)
            for avis in aviss:
                TabCodifications.append(avis.codification)

        if len(TabCodifications) == 0:
            return Response({'codification': False})

        liste = ['RMQ', 'FA', 'F', 'HM', 'SO', 'VI']
        unique_liste = list(set(TabCodifications))
        codification = unique_liste[0]

        for tu in unique_liste:
            if liste.index(tu) < liste.index(codification):
                codification = tu

        return Response({'codification': codification})

class GetAllDetailDocument(APIView):
    def get(self, request, id_affaire):
        all_document = Documents.objects.all()

        data = []

        for document in all_document:
            emetteur = document.emetteur
            if emetteur != None:
                affaireOuvrage = emetteur.affaire_ouvrage
                affaireEntreprise = emetteur.affaire_entreprise

                id = affaireOuvrage.id_affaire.id
                if id == id_affaire:
                    prepare = model_to_dict(document)
                    ouvrage = affaireOuvrage.id_ouvrage
                    print(ouvrage)
                    entreprise = affaireEntreprise.entreprise

                    prepare['ouvrage'] = model_to_dict(ouvrage)
                    prepare['entreprise'] = model_to_dict(entreprise)

                    data.append(prepare)

        return Response(data)
    
class GetAllDetailDocumentWithIdDoc(APIView):
    def get(self, request, id_affaire, id_doc):
        all_document = Documents.objects.all()
        data = []

        for document in all_document:
            emetteur = document.emetteur
            if emetteur is not None:
                affaireOuvrage = emetteur.affaire_ouvrage
                affaireEntreprise = emetteur.affaire_entreprise

                id = affaireOuvrage.id_affaire.id
                if id == id_affaire:
                    prepare = model_to_dict(document)
                    ouvrage = affaireOuvrage.id_ouvrage
                    entreprise = affaireEntreprise.entreprise

                    prepare['ouvrage'] = model_to_dict(ouvrage)
                    prepare['entreprise'] = model_to_dict(entreprise)

                    data.append(prepare)

        if id_doc is not None:
            filtered_data = [doc for doc in data if doc['id'] == id_doc]
            if len(filtered_data) == 0:
                return Response({'error': 'Document not found'}, status=404)
            return Response(filtered_data[0])
        
        return Response(data)


class CheckAvisOnDocumentByCollaborateur(APIView):
    def get(self, request, id_document, id_collaborateur):
        all_avis = Avis.objects.all()
        find = None
        for avis in all_avis:
            document = avis.id_document
            collab = avis.collaborateurs
            if document.id == id_document and collab.id == id_collaborateur:
                find = avis
                break

        if find == None:
            return Response({'avis' : False})
        else:
            return Response({'avis' : model_to_dict(find)})


class RecupereLensembleDesAvisSurDocument(APIView):
    def get(self, request, id_document):
        aviss = Avis.objects.all()
        TabCodifications = []
        for avis in aviss:
            document = avis.id_document
            if id_document == document.id:
                TabCodifications.append(avis.codification)
        if len(TabCodifications) == 0:
            return Response({'codification': False})
        liste = ['RMQ', 'FA', 'F', 'HM', 'SO', 'VI']
        unique_liste = list(set(TabCodifications))
        codification = unique_liste[0]

        for tu in unique_liste:
            if liste.index(tu) < liste.index(codification):
                codification = tu

        return Response({'codification': codification})


class GetAffaireOuvrageFromDocument(APIView):
    def get(self, request, id_doc):
        try:
            doc = Documents.objects.get(id=id_doc)
            entreprise_affaire_ouvrage = doc.emetteur

            affaire_ouvrage = entreprise_affaire_ouvrage.affaire_ouvrage
            result = model_to_dict(affaire_ouvrage)
            if affaire_ouvrage.validateur:
                result['detail_validateur'] = model_to_dict(affaire_ouvrage.validateur)
            return Response(result)
        except:
            return Response({'not found' : True})

class GetAllDetailAsoForAffaire(APIView):
    def get(self, request, id_affaire):
        all_aso = Aso.objects.all()

        data = []

        for aso in all_aso:
            affaire = aso.affaireouvrage.id_affaire
            if affaire.id == id_affaire:
                prepare = model_to_dict(aso)
                prepare['ouvrage'] = model_to_dict(aso.affaireouvrage.id_ouvrage)
                data.append(prepare)
        
        return Response(data)
    
class GetAllDetailAsoForAffaireOneVersion(APIView):
    def get(self, request, id_aso):
        try:
            aso = Aso.objects.get(id=id_aso)
            data = model_to_dict(aso)
            data['ouvrage'] = model_to_dict(aso.affaireouvrage.id_ouvrage)
            return Response(data)
        except:
            return Response({'not found' : True})

class GetAllDetailDocumentForAffaireOuvrage(APIView):
    def get(self, request, id_affaire_ouvrage):
        all_doc = Documents.objects.filter(aso=None);

        data = []
        for doc in all_doc:
            if doc.emetteur != None:
                affaire_ouvrage = doc.emetteur.affaire_ouvrage
                if affaire_ouvrage.id == id_affaire_ouvrage:
                    prepare = model_to_dict(doc)
                    prepare['ouvrage'] = model_to_dict(doc.emetteur.affaire_ouvrage.id_ouvrage)
                    prepare['entreprise'] = model_to_dict(doc.emetteur.affaire_entreprise.entreprise)
                    data.append(prepare)
        return Response(data)
    

class GetAllDetailDocumentForAffaireOuvrageAsoVersion(APIView):
    def get(self, request, id_aso):
        all_doc = Documents.objects.filter(aso=id_aso);

        data = []
        for doc in all_doc:
            prepare = model_to_dict(doc)
            prepare['ouvrage'] = model_to_dict(doc.emetteur.affaire_ouvrage.id_ouvrage)
            prepare['entreprise'] = model_to_dict(doc.emetteur.affaire_entreprise.entreprise)
            data.append(prepare)
        return Response(data)
    
class GenerateDataForAso(APIView):
    def get(self, request, id_aso):
        try:
            aso = Aso.objects.get(id=id_aso)

            data = {}

            # Donne de l'aso

            data['aso'] = model_to_dict(aso)

            # Donne de l'affaire

            data['affaire'] = model_to_dict(aso.affaireouvrage.id_affaire)

            # Donne ouvrage et entreprise en diffusion

            data['ouvrage'] = model_to_dict(aso.affaireouvrage.id_ouvrage)
            data['collaborateurs'] = []

            entreprise_affaire = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=aso.affaireouvrage.id, diffusion=True)
            for ea in entreprise_affaire:
                data['collaborateurs'].append(model_to_dict(ea.affaire_entreprise.entreprise))
            # Donne du charge d'affaire

            charge = aso.affaireouvrage.id_affaire.charge

            data['charge'] = model_to_dict(charge)
            data['charge']['adresse'] = model_to_dict(charge.address)

            # Donne de l'entreprise cliente

            entreprise = aso.affaireouvrage.id_affaire.client

            data['client'] = model_to_dict(entreprise)
            data['client']['adresse'] = model_to_dict(entreprise.adresse)

            # All mission

            data['mission'] = []
            id_affaire = entreprise = aso.affaireouvrage.id_affaire.id

            all_mission = MissionActive.objects.filter(id_affaire=id_affaire)

            for mission in all_mission:
                data['mission'].append(model_to_dict(mission.id_mission))

            # Data about document

            data['documents'] = []
            
            all_entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=aso.affaireouvrage)
            all_document = Documents.objects.filter(aso=id_aso)
            all_commentaire = Commentaire.objects.all()
            aviss = Avis.objects.all()
            liste = ['RMQ', 'FA', 'F', 'HM', 'SO', 'VI']


            for document in all_document:
                for e_a_o in all_entreprise_affaire_ouvrage:
                    if document.emetteur != None and document.emetteur.id == e_a_o.id:
                        prepare = {}
                        prepare['document'] = model_to_dict(document)
                        prepare['avis'] = []
                        for commentaire in all_commentaire:
                            if commentaire.id_avis.id_document.id == document.id:
                                prepare['avis'].append(model_to_dict(commentaire))

                        TabCodifications = []
                        for avis in aviss:
                            document_o = avis.id_document
                            if document.id == document_o.id:
                                TabCodifications.append(avis.codification)
                        if len(TabCodifications) != 0:
                            unique_liste = list(set(TabCodifications))
                            codification = unique_liste[0]

                            for tu in unique_liste:
                                if liste.index(tu) < liste.index(codification):
                                    codification = tu
                            prepare['codification'] = codification
                        
                        data['documents'].append(prepare)

            aviss = Avis.objects.all()
            TabCodifications = []
            for avis in aviss:
                print(avis.id)
                document = avis.id_document
                if document.aso.id == id_aso:
                    TabCodifications.append(avis.codification)

            liste = ['RMQ', 'FA', 'F', 'HM', 'SO', 'VI']
            unique_liste = list(set(TabCodifications))
            codification = unique_liste[0]

            for tu in unique_liste:
                if liste.index(tu) < liste.index(codification):
                    codification = tu

            data['codification'] = codification
        
            return Response(data)
        
        except:
            return Response({})

            

class CheckIfCanValidateAffaireOuvrage(APIView):
    def get(self, request, id_affaire_ouvrage):
        affaire_ouvrage = AffaireOuvrage.objects.get(id=id_affaire_ouvrage)
        entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=affaire_ouvrage)
        documents = Documents.objects.filter(emetteur__in=entreprise_affaire_ouvrage, aso=None)
        
        if not documents:
            return Response({"can_validate": False, "reason": "No unprocessed documents found"})
        
        for document in documents:
            avis_exists = Avis.objects.filter(id_document=document).exists()
            if not avis_exists:
                return Response({"can_validate": False, "reason": "Unreviewed document found"})
        
        return Response({"can_validate": True})

class CheckAsoCurrentForAffaireOuvrage(APIView):
    def get(self, request, id_affaire_ouvrage):
        affaire_ouvrage = AffaireOuvrage.objects.get(id=id_affaire_ouvrage)
        aso_exists = Aso.objects.filter(affaireouvrage=affaire_ouvrage, statut=0).exists()
        
        if aso_exists:
            return Response({"has_current_aso": True})
        
        return Response({"has_current_aso": False})

class AllEntrepriseConcerneByAso(APIView):
    def get(self, request, id_aso):
        aso = Aso.objects.get(id=id_aso)

        affaire_ouvrage = aso.affaireouvrage

        entreprise_affaire_ouvrage = EntrepriseAffaireOuvrage.objects.filter(affaire_ouvrage=affaire_ouvrage.id)

        data = []

        for eao in entreprise_affaire_ouvrage:
            result = model_to_dict(eao)
            result['detail_entreprise'] = model_to_dict(eao.affaire_entreprise.entreprise)
            result['responsables'] = []
            responsables = Responsable.objects.filter(entreprise=eao.affaire_entreprise.entreprise.id)
            for responsable in responsables:
                result['responsables'].append(model_to_dict(responsable))
            data.append(result)

        return Response(data)
    

class AffaireOuvrageConcerneByAso(APIView):
    def get(self, request, id_aso):
        aso = Aso.objects.get(id=id_aso)

        return Response(model_to_dict(aso.affaireouvrage))